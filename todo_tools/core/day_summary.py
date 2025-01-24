from rich.table import Table
from todo_tools.utils.time_utils import parse_duration
from todo_tools.utils.table_utils import console
from todo_tools.utils.config import config

class DaySummary:
    def __init__(self, task_manager, todo_manager):
        self.task_manager = task_manager
        self.todo_manager = todo_manager

    def show_summary(self):
        """显示今日总结"""
        if not self.task_manager.tasks:
            console.print("[yellow]今日暂无任务记录[/yellow]")
            return

        # 创建总结表格
        table = Table(title="📊 今日总结", title_style="bold blue", show_lines=True)
        
        # 添加列
        table.add_column("指标", style="cyan")
        table.add_column("数值", style="green")
        
        # 计算统计数据
        total_tasks = len(self.task_manager.tasks)
        completed_tasks = len([t for t in self.task_manager.tasks.values() if t.status == "completed"])
        
        # 计算平均满意度
        satisfaction_scores = [t.satisfaction for t in self.task_manager.tasks.values() if t.status == "completed"]
        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
        
        # 计算时间统计
        total_planned_seconds = 0
        total_actual_seconds = 0
        
        for task in self.task_manager.tasks.values():
            if task.status == "completed":
                # 计划时间
                planned_seconds = parse_duration(task.planned_time)
                total_planned_seconds += planned_seconds
                
                # 实际时间
                actual_seconds = parse_duration(task.task_len)
                total_actual_seconds += actual_seconds
        
        time_ratio = (total_actual_seconds / total_planned_seconds * 100) if total_planned_seconds > 0 else 0
        
        # 待办事项完成度
        total_todos = len([t for t in self.todo_manager.todos.values() if t.status != "deleted"])
        completed_todos = len([t for t in self.todo_manager.todos.values() if t.status == "completed"])
        todo_completion = (completed_todos / total_todos * 100) if total_todos > 0 else 0
        
        # 添加数据行
        table.add_row("总任务数", f"{total_tasks}")
        table.add_row("已完成任务", f"{completed_tasks}/{total_tasks} ({completed_tasks/total_tasks*100:.1f}%)")
        table.add_row("平均满意度", f"{avg_satisfaction:.1f}⭐")
        table.add_row("计划总时长", f"{total_planned_seconds//3600}h{(total_planned_seconds%3600)//60}m")
        table.add_row("实际总时长", f"{total_actual_seconds//3600}h{(total_actual_seconds%3600)//60}m")
        table.add_row("时间效率比", f"{time_ratio:.1f}%")
        table.add_row("待办完成率", f"{completed_todos}/{total_todos} ({todo_completion:.1f}%)")
        
        console.print(table) 