from flask import Flask, jsonify, request, send_from_directory
from todo_tools.core.task_manager import TaskManager
from todo_tools.core.todo_manager import TodoManager
from todo_tools.core.file_manager import init_filepath
from todo_tools.utils.config import config
import webbrowser
import threading
import time
import os
import signal
import sys
from datetime import datetime
from pathlib import Path
import json

app = Flask(__name__, static_folder='static')
server_running = True

# 开发模式配置
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# HTML内容
HTML_CONTENT = ''

# 初始化管理器
init_filepath()
task_manager = TaskManager()
todo_manager = TodoManager(task_manager)

@app.route('/')
def index():
    """返回HTML内容"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/dates')
def get_available_dates():
    try:
        # 遍历数据目录获取所有可用日期
        data_dir = Path('data')
        dates = set()  # 使用集合避免重复
        
        # 添加今天的日期
        today = datetime.now().strftime('%Y-%m-%d')
        dates.add(today)
        
        # 添加历史数据的日期
        for year_dir in sorted(data_dir.glob('*')):
            if year_dir.is_dir():
                for month_dir in sorted(year_dir.glob('*')):
                    if month_dir.is_dir():
                        for todo_file in sorted(month_dir.glob('*_todo.json')):
                            date_str = todo_file.stem.replace('_todo', '')
                            dates.add(date_str)
        
        # 转换为列表并排序
        dates_list = sorted(list(dates))
        return jsonify(dates_list)
    except Exception as e:
        print(f"Error getting available dates: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/data/<date>')
def get_data(date):
    try:
        # 将 YYYY-MM-DD 格式转换为文件路径
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        year = date_obj.strftime('%Y')
        month = date_obj.strftime('%m')
        date_str = date_obj.strftime('%Y-%m-%d')
        
        # 构建文件路径 - 使用绝对路径
        base_dir = Path(__file__).parent.parent.parent
        data_dir = base_dir / 'data' / year / month
        todo_file = data_dir / f'{date_str}_todo.json'
        tasks_file = data_dir / f'{date_str}_tasks.json'
        
        print(f"Looking for files at: {todo_file} and {tasks_file}")  # 调试信息
        
        todos = {}
        tasks = {}
        
        # 如果是今天的日期，从内存中获取数据
        today = datetime.now().strftime('%Y-%m-%d')
        if date_str == today:
            todos = {str(k): v.__dict__ for k, v in todo_manager.todos.items()}
            tasks = {str(k): v.__dict__ for k, v in task_manager.tasks.items()}
        else:
            # 从文件读取历史数据
            try:
                if todo_file.exists():
                    with open(todo_file, 'r', encoding='utf-8') as f:
                        todos = json.load(f)
                    print(f"Loaded todos: {len(todos)} items")  # 调试信息
                else:
                    print(f"Todo file not found: {todo_file}")  # 调试信息
                    
                if tasks_file.exists():
                    with open(tasks_file, 'r', encoding='utf-8') as f:
                        tasks = json.load(f)
                        # 确保 feeling 字段存在
                        for task in tasks.values():
                            task['feeling'] = task.get('summary', '')  # 将 summary 映射到 feeling
                    print(f"Loaded tasks: {len(tasks)} items")  # 调试信息
                else:
                    print(f"Tasks file not found: {tasks_file}")  # 调试信息
            except Exception as e:
                print(f"Error reading files: {str(e)}")
                raise
        
        # 计算统计数据
        completed_todos = len([t for t in todos.values() if t.get('status') == 'completed'])
        total_todos = len(todos)
        
        completion_rate = round((completed_todos / total_todos * 100) if total_todos > 0 else 0)
        
        # 计算平均满意度
        satisfaction_scores = [t.get('satisfaction', 0) for t in tasks.values()]
        avg_satisfaction = round(sum(satisfaction_scores) / len(satisfaction_scores), 1) if satisfaction_scores else 0
        
        # 计算时间效率
        def parse_time_to_minutes(time_str):
            if not time_str:
                return 0
            try:
                if 'h' in time_str and ('min' in time_str or 'm' in time_str):
                    hours = int(time_str.split('h')[0])
                    minutes = int(''.join(filter(str.isdigit, time_str.split('h')[1])))
                    return hours * 60 + minutes
                elif 'h' in time_str:
                    hours = int(time_str.replace('h', ''))
                    return hours * 60
                elif 'min' in time_str or 'm' in time_str:
                    minutes = int(''.join(filter(str.isdigit, time_str)))
                    return minutes
                return 0
            except:
                return 0

        planned_times = sum([parse_time_to_minutes(t.get('planned_time', '0min')) for t in tasks.values()])
        actual_times = sum([parse_time_to_minutes(t.get('task_len', '0min')) for t in tasks.values()])
        
        time_efficiency = round((planned_times / actual_times * 100) if actual_times > 0 else 0)
        
        response_data = {
            'todos': todos,
            'tasks': tasks,
            'stats': {
                'completion_rate': completion_rate,
                'avg_satisfaction': avg_satisfaction,
                'time_efficiency': time_efficiency,
                'completed_todos': completed_todos,
                'total_todos': total_todos,
                'planned_time': planned_times,
                'actual_time': actual_times
            }
        }
        
        print(f"Returning data for {date_str}: {len(todos)} todos, {len(tasks)} tasks")  # 调试信息
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error processing data for date {date}: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/todos/<todo_id>', methods=['PUT', 'DELETE'])
def manage_todo(todo_id):
    """管理待办事项"""
    try:
        if request.method == 'DELETE':
            if todo_id in todo_manager.todos:
                todo_manager.todos[todo_id].status = "deleted"
                todo_manager.save_todos()
                return jsonify({"status": "success"})
            return jsonify({"status": "error", "message": "Todo not found"}), 404
        
        elif request.method == 'PUT':
            data = request.json
            if todo_id in todo_manager.todos:
                todo = todo_manager.todos[todo_id]
                if 'name' in data:
                    todo.name = data['name']
                if 'time' in data:
                    todo.time = data['time']
                if 'importance' in data:
                    todo.importance = data['importance']
                todo_manager.save_todos()
                return jsonify({"status": "success"})
            return jsonify({"status": "error", "message": "Todo not found"}), 404
            
    except Exception as e:
        print(f"Error managing todo {todo_id}: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

def signal_handler(signum, frame):
    """处理中断信号"""
    global server_running
    print("\n正在停止服务器...")
    server_running = False
    sys.exit(0)

def open_browser():
    """在新线程中打开浏览器"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:10066')

def start_server():
    """启动Web服务器"""
    global server_running
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        app.run(host='0.0.0.0', port=10066, debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("\n正在停止服务器...")
        sys.exit(0)
    finally:
        server_running = False 

def parse_time_to_minutes(time_str):
    """将时间字符串转换为分钟数"""
    try:
        if 'h' in time_str and 'min' in time_str:
            hours, minutes = time_str.split('h')
            minutes = minutes.replace('min', '')
            return int(hours) * 60 + int(minutes)
        elif 'h' in time_str:
            hours = time_str.replace('h', '')
            return int(hours) * 60
        elif 'min' in time_str:
            minutes = time_str.replace('min', '')
            return int(minutes)
        return 0
    except:
        return 0 