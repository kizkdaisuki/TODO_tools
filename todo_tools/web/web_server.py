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

@app.route('/api/dates', methods=['GET'])
def get_available_dates():
    """获取可用的日期列表"""
    # 获取当前日期
    today = datetime.now().strftime('%Y-%m-%d')
    return jsonify([today])

@app.route('/api/data/<date>', methods=['GET'])
def get_date_data(date):
    """获取指定日期的数据"""
    try:
        # 获取数据
        tasks = {k: v.to_dict() for k, v in task_manager.tasks.items()}
        todos = {k: v.to_dict() for k, v in todo_manager.todos.items()}
        
        # 确保任务数据包含感受字段
        for task_id, task in tasks.items():
            task['feeling'] = task.get('feeling', '')  # 添加感受字段
            
        summary = task_manager.day_summary.get_summary_data()
        
        return jsonify({
            "tasks": tasks,
            "todos": todos,
            "summary": summary
        })
    except Exception as e:
        print(f"Error getting data for date {date}: {e}")
        return jsonify({
            "tasks": {},
            "todos": {},
            "summary": {
                "completed_tasks": 0,
                "total_tasks": 0,
                "completed_todos": 0,
                "total_todos": 0,
                "avg_satisfaction": 0,
                "completion_rate": 0,
                "time_efficiency": 0,
                "planned_time": 0,
                "actual_time": 0
            }
        })

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