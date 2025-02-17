from flask import Flask, send_from_directory, jsonify
from todo_tools.core.task_manager import TaskManager
from todo_tools.core.todo_manager import TodoManager
from todo_tools.core.file_manager import init_filepath
import webbrowser
import threading
import time
import os
import signal
import sys

app = Flask(__name__)
server_running = True

# 开发模式配置
app.config['DEBUG'] = True  # 启用调试模式
app.config['TEMPLATES_AUTO_RELOAD'] = True  # 模板自动重载
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0  # 禁用缓存

# HTML内容
HTML_CONTENT = '''<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TODO Dashboard</title>
    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .glass {
            background: rgba(255, 255, 255, 0.2);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        .fade-enter-active,
        .fade-leave-active {
            transition: opacity 0.3s ease;
        }
        
        .fade-enter-from,
        .fade-leave-to {
            opacity: 0;
        }
    </style>
</head>
<body class="p-6">
    <div id="app" class="max-w-7xl mx-auto">
        <!-- 标题 -->
        <h1 class="text-4xl font-bold text-white mb-8 text-center">TODO Dashboard</h1>
        
        <!-- 统计卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <div class="glass rounded-xl p-6 text-white">
                <h3 class="text-lg font-semibold mb-2">任务完成率</h3>
                <p class="text-3xl font-bold">{{ completionRate }}%</p>
            </div>
            <div class="glass rounded-xl p-6 text-white">
                <h3 class="text-lg font-semibold mb-2">平均满意度</h3>
                <p class="text-3xl font-bold">{{ avgSatisfaction }}⭐</p>
            </div>
            <div class="glass rounded-xl p-6 text-white">
                <h3 class="text-lg font-semibold mb-2">时间效率</h3>
                <p class="text-3xl font-bold">{{ timeEfficiency }}%</p>
            </div>
        </div>
        
        <!-- 切换按钮 -->
        <div class="flex justify-center mb-8 space-x-4">
            <button 
                @click="currentView = 'todos'"
                :class="['px-6 py-2 rounded-full transition-all duration-300', 
                        currentView === 'todos' 
                            ? 'bg-white text-purple-600 shadow-lg' 
                            : 'glass text-white hover:bg-white/30']">
                待办事项
            </button>
            <button 
                @click="currentView = 'tasks'"
                :class="['px-6 py-2 rounded-full transition-all duration-300', 
                        currentView === 'tasks' 
                            ? 'bg-white text-purple-600 shadow-lg' 
                            : 'glass text-white hover:bg-white/30']">
                已完成任务
            </button>
        </div>
        
        <!-- 数据表格 -->
        <div class="glass rounded-xl p-6">
            <div v-if="currentView === 'todos'">
                <!-- 待办事项表格 -->
                <table class="w-full text-white">
                    <thead>
                        <tr class="border-b border-white/20">
                            <th class="py-3 text-left">任务名称</th>
                            <th class="py-3 text-left">预计时长</th>
                            <th class="py-3 text-left">重要性</th>
                            <th class="py-3 text-left">状态</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="todo in todos" 
                            :key="todo.id" 
                            class="border-b border-white/10 hover:bg-white/10 transition-colors">
                            <td class="py-3">{{ todo.name }}</td>
                            <td class="py-3">{{ todo.time }}</td>
                            <td class="py-3">{{ todo.importance }}</td>
                            <td class="py-3">
                                <span :class="todo.status === 'completed' ? 'text-green-400' : 'text-yellow-400'">
                                    {{ todo.status === 'completed' ? '✅ 已完成' : '🕒 待完成' }}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div v-else>
                <!-- 已完成任务表格 -->
                <table class="w-full text-white">
                    <thead>
                        <tr class="border-b border-white/20">
                            <th class="py-3 text-left">任务名称</th>
                            <th class="py-3 text-left">开始时间</th>
                            <th class="py-3 text-left">结束时间</th>
                            <th class="py-3 text-left">计划时长</th>
                            <th class="py-3 text-left">实际时长</th>
                            <th class="py-3 text-left">重要性</th>
                            <th class="py-3 text-left">满意度</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="task in tasks" 
                            :key="task.task_id" 
                            class="border-b border-white/10 hover:bg-white/10 transition-colors">
                            <td class="py-3">{{ task.task_name }}</td>
                            <td class="py-3">{{ task.start_time }}</td>
                            <td class="py-3">{{ task.end_time }}</td>
                            <td class="py-3">{{ task.planned_time }}</td>
                            <td class="py-3">{{ task.task_len }}</td>
                            <td class="py-3">{{ task.importance }}</td>
                            <td class="py-3">{{ '⭐'.repeat(task.satisfaction) }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- 图表 -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
            <div class="glass rounded-xl p-6">
                <canvas id="completionChart"></canvas>
            </div>
            <div class="glass rounded-xl p-6">
                <canvas id="timeChart"></canvas>
            </div>
        </div>
    </div>

    <script>
        const { createApp, onMounted, ref } = Vue

        createApp({
            setup() {
                const currentView = ref('todos')
                const todos = ref([])
                const tasks = ref([])
                const completionRate = ref(0)
                const avgSatisfaction = ref(0)
                const timeEfficiency = ref(0)
                
                // 获取数据
                const fetchData = async () => {
                    const [todosRes, tasksRes, summaryRes] = await Promise.all([
                        fetch('/api/todos').then(r => r.json()),
                        fetch('/api/tasks').then(r => r.json()),
                        fetch('/api/summary').then(r => r.json())
                    ])
                    
                    todos.value = Object.values(todosRes)
                    tasks.value = Object.values(tasksRes)
                    
                    // 更新统计数据
                    completionRate.value = summaryRes.completion_rate
                    avgSatisfaction.value = summaryRes.avg_satisfaction
                    timeEfficiency.value = summaryRes.time_efficiency
                    
                    // 更新图表
                    updateCharts(summaryRes)
                }
                
                // 初始化图表
                const updateCharts = (data) => {
                    // 任务完成情况图表
                    new Chart(document.getElementById('completionChart'), {
                        type: 'doughnut',
                        data: {
                            labels: ['已完成', '未完成'],
                            datasets: [{
                                data: [data.completed_tasks, data.total_tasks - data.completed_tasks],
                                backgroundColor: ['rgba(34, 197, 94, 0.8)', 'rgba(255, 255, 255, 0.2)']
                            }]
                        },
                        options: {
                            plugins: {
                                legend: {
                                    labels: {
                                        color: 'white'
                                    }
                                }
                            }
                        }
                    })
                    
                    // 时间效率图表
                    new Chart(document.getElementById('timeChart'), {
                        type: 'bar',
                        data: {
                            labels: ['计划时长', '实际时长'],
                            datasets: [{
                                data: [data.planned_time, data.actual_time],
                                backgroundColor: ['rgba(255, 255, 255, 0.5)', 'rgba(147, 51, 234, 0.5)']
                            }]
                        },
                        options: {
                            plugins: {
                                legend: {
                                    display: false
                                }
                            },
                            scales: {
                                y: {
                                    ticks: {
                                        color: 'white'
                                    }
                                },
                                x: {
                                    ticks: {
                                        color: 'white'
                                    }
                                }
                            }
                        }
                    })
                }
                
                onMounted(() => {
                    fetchData()
                    // 每分钟刷新一次数据
                    setInterval(fetchData, 60000)
                })
                
                return {
                    currentView,
                    todos,
                    tasks,
                    completionRate,
                    avgSatisfaction,
                    timeEfficiency
                }
            }
        }).mount('#app')
    </script>
</body>
</html>
'''

# 初始化管理器
init_filepath()
task_manager = TaskManager()
todo_manager = TodoManager(task_manager)

@app.route('/')
def index():
    """返回HTML内容"""
    return HTML_CONTENT

@app.route('/api/tasks')
def get_tasks():
    """获取所有任务"""
    tasks = {k: v.to_dict() for k, v in task_manager.tasks.items()}
    return jsonify(tasks)

@app.route('/api/todos')
def get_todos():
    """获取所有待办事项"""
    todos = {k: v.to_dict() for k, v in todo_manager.todos.items()}
    return jsonify(todos)

@app.route('/api/summary')
def get_summary():
    """获取任务总结"""
    return jsonify(task_manager.day_summary.get_summary_data())

def signal_handler(signum, frame):
    """处理中断信号"""
    global server_running
    print("\n正在停止服务器...")
    server_running = False
    sys.exit(0)

def open_browser():
    """在新线程中打开浏览器"""
    time.sleep(1.5)
    webbrowser.open('http://localhost:5000')

def start_server():
    """启动Web服务器"""
    global server_running
    
    # 注册信号处理
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 启动浏览器
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        # 修改host参数，允许所有网络接口访问
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
    except KeyboardInterrupt:
        print("\n正在停止服务器...")
        sys.exit(0)
    finally:
        server_running = False 