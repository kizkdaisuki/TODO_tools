"""表格工具"""
from rich.console import Console
from rich.table import Table
from todo_tools.utils.config import config

console = Console()

def generate_task_table(tasks: dict) -> Table:
    """生成任务表格"""
    table = Table(
        title="今日任务记录", 
        title_style="bold blue",
        show_lines=True
    )
    
    # 添加列
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("任务名称", style="green")
    table.add_column("开始时间", style="magenta")
    table.add_column("结束时间", style="magenta")
    table.add_column("时长", style="yellow")
    table.add_column("重要性", justify="center")
    table.add_column("满意度", justify="center")
    table.add_column("状态", style="blue")
    table.add_column("感受", style="green", max_width=30)
    
    # 添加数据
    for task in tasks.values():
        # 处理满意度显示
        satisfaction_display = (
            config.DICT_SATISFACTION[task.satisfaction] 
            if task.satisfaction in config.DICT_SATISFACTION 
            else "待评分"
        )
        
        table.add_row(
            str(task.task_id),
            task.name,
            task.start_time,
            task.end_time,
            task.task_len,
            config.DICT_IMPORTANCE[task.importance],
            satisfaction_display,
            task.status,
            task.summary or ""  # 如果 summary 为 None，显示空字符串
        )
    
    return table

def generate_todo_table(todos: dict) -> Table:
    """生成待办事项表格"""
    table = Table(title="待办事项列表", title_style="bold blue", show_lines=True)
    
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("任务名称", style="green")
    table.add_column("预计时长", style="magenta")
    table.add_column("重要性", justify="center")
    table.add_column("状态", style="blue")
    
    for todo_id, todo in todos.items():
        if todo.status != "deleted":
            table.add_row(
                todo_id,
                todo.name,
                todo.time,
                config.DICT_IMPORTANCE[todo.importance],
                "🕒 待完成" if todo.status == "pending" else "✅ 已完成"
            )
    
    return table

def generate_timer_table(task: 'Task', remaining: int, total: int) -> Table:
    """生成计时器表格"""
    table = Table(
        title="🍅 番茄钟",
        title_style="bold magenta",
        show_header=True,
        header_style="bold cyan",
        show_lines=True
    )
    
    table.add_column("任务名称", style="cyan", justify="center")
    table.add_column("剩余时间", style="green", justify="center")
    table.add_column("进度条", style="yellow", justify="center", width=30)
    table.add_column("重要度", style="red", justify="center")
    
    # 计算进度
    if total <= 0:
        progress = 100.0  # 如果总时间为0，则显示100%
    else:
        progress = (total - remaining) / total * 100
    
    blocks = int(progress / 3.333)  # 30个字符宽度
    progress_bar = "█" * blocks + "░" * (30 - blocks)
    
    # 格式化剩余时间
    hours = remaining // 3600
    minutes = (remaining % 3600) // 60
    seconds = remaining % 60
    
    if hours > 0:
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        time_str = f"{minutes:02d}:{seconds:02d}"
    
    table.add_row(
        task.name,
        time_str,
        f"{progress_bar} {progress:>6.1f}%",
        config.DICT_IMPORTANCE[task.importance]
    )
    
    return table 