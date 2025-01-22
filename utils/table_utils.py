"""
表格生成工具
处理表格的生成和显示
"""
from rich.table import Table
from rich.console import Console
from utils.config import DICT_IMPORTANCE, DICT_SATISFACTION

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
        table.add_row(
            str(task['task_id']),
            task['task_name'],
            task['start_time'],
            task['end_time'],
            task['task_len'],
            DICT_IMPORTANCE[task['importance']],
            DICT_SATISFACTION[task['satisfaction']],
            task['status'],
            task.get('summary', '')
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
                DICT_IMPORTANCE[todo.importance],
                "🕒 待完成" if todo.status == "pending" else "✅ 已完成"
            )
    
    return table 