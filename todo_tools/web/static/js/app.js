const { createApp, ref, onMounted, onUnmounted, computed } = Vue

let completionChart = null
let timeChart = null

createApp({
    setup() {
        const currentView = ref('todos')
        const todos = ref([])
        const tasks = ref([])
        const completionRate = ref(0)
        const avgSatisfaction = ref(0)
        const timeEfficiency = ref(0)
        const availableDates = ref([])
        const selectedDate = ref('')
        const editingTodo = ref(null)
        const timeOptions = ref([
            '25min', '45min', '1h', '1h30min', '2h'
        ])
        
        const selectedTask = ref(null)
        
        const currentTheme = ref('dark-purple')
        
        const editMode = ref(false)
        
        const updateCharts = (data) => {
            if (completionChart) {
                completionChart.destroy()
            }
            if (timeChart) {
                timeChart.destroy()
            }
            
            // 待办事项完成情况图表
            completionChart = new Chart(document.getElementById('completionChart'), {
                type: 'doughnut',
                data: {
                    labels: ['已完成', '未完成'],
                    datasets: [{
                        data: [data.completed_todos, data.total_todos - data.completed_todos],
                        backgroundColor: ['#4ade80', 'rgba(255, 255, 255, 0.2)'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: 'white',
                                padding: 20,
                                font: {
                                    size: 14
                                }
                            }
                        },
                        title: {
                            display: true,
                            text: '待办事项完成情况',
                            color: 'white',
                            font: {
                                size: 16,
                                weight: 'normal'
                            },
                            padding: {
                                bottom: 20
                            }
                        }
                    }
                }
            })
            
            // 时间效率对比图表
            timeChart = new Chart(document.getElementById('timeChart'), {
                type: 'bar',
                data: {
                    labels: ['计划时长', '实际时长'],
                    datasets: [{
                        data: [data.planned_time, data.actual_time],
                        backgroundColor: ['rgba(255, 255, 255, 0.7)', 'rgba(147, 51, 234, 0.7)'],
                        borderWidth: 0,
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: '时间效率对比（分钟）',
                            color: 'white',
                            font: {
                                size: 16,
                                weight: 'normal'
                            },
                            padding: {
                                bottom: 20
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: {
                                color: 'rgba(255, 255, 255, 0.1)'
                            },
                            ticks: {
                                color: 'white',
                                font: {
                                    size: 12
                                }
                            }
                        },
                        x: {
                            grid: {
                                display: false
                            },
                            ticks: {
                                color: 'white',
                                font: {
                                    size: 12
                                }
                            }
                        }
                    }
                }
            })
        }

        const showTaskDetail = (task) => {
            // 如果是待办事项且正在编辑，不显示详情
            if (task.id && editingTodo.value === task.id) return
            
            selectedTask.value = {
                ...task,
                // 格式化显示的时间
                start_time: formatters.datetime(task.start_time),
                end_time: formatters.datetime(task.end_time),
                planned_time: formatters.time(task.planned_time),
                task_len: formatters.time(task.task_len),
                importance: formatters.importance(task.importance).text,
                task_name: task.task_name || task.name, // 兼容待办事项和已完成任务
                feeling: task.summary || task.feeling || '暂无感受' // 使用 summary 作为 feeling
            }
        }

        const fetchData = async () => {
            try {
                const response = await fetch(`/api/data/${selectedDate.value}`)
                const data = await response.json()
                
                if (data.error) {
                    throw new Error(data.error)
                }
                
                todos.value = Object.entries(data.todos || {}).map(([id, todo]) => ({
                    id,
                    ...todo
                }))
                
                tasks.value = Object.entries(data.tasks || {}).map(([id, task]) => ({
                    id,
                    ...task
                }))
                
                // 从 stats 对象中获取统计数据
                const stats = data.stats || {
                    completion_rate: 0,
                    avg_satisfaction: 0,
                    time_efficiency: 0,
                    completed_todos: 0,
                    total_todos: 0,
                    planned_time: 0,
                    actual_time: 0
                }
                
                // 直接使用后端计算的时间效率
                completionRate.value = stats.completion_rate
                avgSatisfaction.value = stats.avg_satisfaction
                timeEfficiency.value = stats.time_efficiency
                
                // 更新图表
                updateCharts(stats)

                // 在 fetchData 函数中添加调试信息
                console.log('Backend stats:', data.stats)
                console.log('Time efficiency:', data.stats.time_efficiency)
            } catch (error) {
                console.error('加载数据失败:', error)
                // 设置默认值
                todos.value = []
                tasks.value = []
                completionRate.value = 0
                avgSatisfaction.value = 0
                timeEfficiency.value = 0
            }
        }

        const fetchDates = async () => {
            try {
                const response = await fetch('/api/dates')
                const dates = await response.json()
                
                if (dates.error) {
                    throw new Error(dates.error)
                }
                
                availableDates.value = dates
                
                // 设置默认日期为今天
                const today = new Date().toISOString().split('T')[0]
                if (!selectedDate.value) {
                    selectedDate.value = today
                }
                
                // 如果今天的数据不存在，使用最新的可用日期
                if (!dates.includes(today) && dates.length > 0) {
                    selectedDate.value = dates[dates.length - 1]
                }
                
                // 加载选中日期的数据
                await fetchData()
            } catch (error) {
                console.error('获取日期列表失败:', error)
                // 设置默认日期
                const today = new Date().toISOString().split('T')[0]
                selectedDate.value = today
                availableDates.value = [today]
            }
        }

        const saveTodo = async (todo) => {
            if (!todo.id) {
                console.error('Todo ID is missing')
                return
            }
            
            try {
                const response = await fetch(`/api/todos/${todo.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        name: todo.name,
                        time: todo.time,
                        importance: todo.importance
                    })
                })
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }
                
                editingTodo.value = null
                await fetchData()
            } catch (error) {
                console.error('保存失败:', error)
                alert('保存失败，请重试')
            }
        }

        const deleteTodo = async (todoId) => {
            if (!todoId) {
                console.error('Todo ID is missing')
                return
            }
            
            if (!confirm('确定要删除这个待办事项吗？')) return
            
            try {
                const response = await fetch(`/api/todos/${todoId}`, {
                    method: 'DELETE'
                })
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }
                
                await fetchData()
            } catch (error) {
                console.error('删除失败:', error)
                alert('删除失败，请重试')
            }
        }

        const changeTheme = (theme) => {
            currentTheme.value = theme
            document.body.dataset.theme = theme
            localStorage.setItem('todo-theme', theme)
        }

        const toggleEditMode = () => {
            editMode.value = !editMode.value
        }

        // 添加格式化函数
        const formatters = {
            time: (time) => {
                if (!time) return '-'
                // 处理 "0h30m9s" 格式
                if (time.includes('s')) {
                    const matches = time.match(/(\d+h)?(\d+m)?(\d+s)?/)
                    if (matches) {
                        const hours = matches[1] ? matches[1].replace('h', '小时') : ''
                        const minutes = matches[2] ? matches[2].replace('m', '分钟') : ''
                        return hours + minutes
                    }
                }
                // 处理 "1h30min" 格式
                return time
                    .replace('h', '小时')
                    .replace('min', '分钟')
            },
            
            datetime: (datetime) => {
                if (!datetime) return '-'
                try {
                    // 如果只有时间没有日期，添加当前日期
                    if (datetime.length <= 8 && datetime.includes(':')) {
                        const today = new Date().toISOString().split('T')[0]
                        datetime = `${today} ${datetime}`
                    }
                    
                    const date = new Date(datetime)
                    if (isNaN(date.getTime())) return datetime // 如果转换失败，直接显示原始时间
                    
                    return date.toLocaleString('zh-CN', {
                        month: 'long',
                        day: 'numeric',
                        hour: '2-digit',
                        minute: '2-digit'
                    })
                } catch (error) {
                    console.error('时间格式化错误:', error)
                    return datetime // 发生错误时显示原始时间
                }
            },
            
            importance: (level) => {
                const map = {
                    'low': { text: '低优先级', color: '#94A3B8' },
                    'mid': { text: '中优先级', color: '#F59E0B' },
                    'high': { text: '高优先级', color: '#EF4444' }
                }
                return map[level] || { text: level, color: '#94A3B8' }
            },
            
            summary: (text) => {
                if (!text) return ''
                // 保留5个字符，超出部分用...替换
                const maxLength = 5
                const trimmed = text.trim()
                return trimmed.length > maxLength 
                    ? trimmed.substring(0, maxLength) + '...'
                    : trimmed
            },
            
            shortTime: (time) => {
                if (!time) return '-'
                // 只显示时:分
                const matches = time.match(/(\d{1,2}):(\d{1,2})/)
                if (matches) {
                    return `${matches[1]}:${matches[2]}`
                }
                return time
            }
        }

        // 在 setup 中添加排序函数
        const sortedTodos = computed(() => {
            // 首先按完成状态分组
            const completed = []
            const uncompleted = []
            
            todos.value.forEach(todo => {
                if (todo.status === 'completed') {
                    completed.push(todo)
                } else {
                    uncompleted.push(todo)
                }
            })
            
            // 对未完成的待办事项按重要性排序
            const importanceOrder = { 'high': 0, 'mid': 1, 'low': 2 }
            uncompleted.sort((a, b) => {
                return importanceOrder[a.importance] - importanceOrder[b.importance]
            })
            
            // 已完成的按完成时间倒序
            completed.sort((a, b) => {
                return new Date(b.completed_time) - new Date(a.completed_time)
            })
            
            // 返回合并后的数组
            return [...uncompleted, ...completed]
        })

        const deleteTask = async (taskId) => {
            if (!taskId) {
                console.error('Task ID is missing')
                return
            }
            
            if (!confirm('确定要删除这个任务吗？')) return
            
            try {
                const response = await fetch(`/api/tasks/${taskId}`, {
                    method: 'DELETE'
                })
                
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`)
                }
                
                await fetchData()
            } catch (error) {
                console.error('删除失败:', error)
                alert('删除失败，请重试')
            }
        }

        const hasNextDay = computed(() => {
            const today = new Date().toISOString().split('T')[0]
            return selectedDate.value < today
        })

        const hasPreviousDay = computed(() => {
            // 移除对 availableDates 的检查，允许选择任何历史日期
            return true
        })

        const navigateDate = async (direction) => {
            const currentDate = new Date(selectedDate.value)
            currentDate.setDate(currentDate.getDate() + direction)
            const newDate = currentDate.toISOString().split('T')[0]
            
            // 只检查是否超过今天
            const today = new Date().toISOString().split('T')[0]
            if (newDate > today) return
            
            selectedDate.value = newDate
            await fetchData()
        }

        onMounted(() => {
            fetchDates()
            // 从 localStorage 恢复主题设置
            const savedTheme = localStorage.getItem('todo-theme')
            if (savedTheme) {
                changeTheme(savedTheme)
            }
        })

        onUnmounted(() => {
            if (completionChart) {
                completionChart.destroy()
            }
            if (timeChart) {
                timeChart.destroy()
            }
        })

        return {
            currentView,
            todos,
            tasks,
            completionRate,
            avgSatisfaction,
            timeEfficiency,
            availableDates,
            selectedDate,
            editingTodo,
            timeOptions,
            loadDateData: fetchData,
            saveTodo,
            deleteTodo,
            selectedTask,
            showTaskDetail,
            currentTheme,
            changeTheme,
            editMode,
            toggleEditMode,
            formatters,
            sortedTodos,
            deleteTask,
            hasNextDay,
            hasPreviousDay,
            navigateDate
        }
    }
}).mount('#app') 