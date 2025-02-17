from rich.table import Table
from todo_tools.utils.time_utils import parse_duration
from todo_tools.utils.table_utils import console
from todo_tools.utils.config import config

class DaySummary:
    def __init__(self, task_manager, todo_manager):
        self.task_manager = task_manager
        self.todo_manager = todo_manager

    def get_summary_data(self):
        """获取汇总数据"""
        # 获取所有任务和待办事项
        tasks = self.task_manager.tasks.values()
        todos = [t for t in self.todo_manager.todos.values() if t.status != "deleted"]
        
        # 计算任务统计
        completed_tasks = len([t for t in tasks if t.status == "completed"])
        total_tasks = len(tasks)
        
        # 计算待办事项统计
        completed_todos = len([t for t in todos if t.status == "completed"])
        total_todos = len(todos)
        
        # 计算满意度
        satisfaction_sum = sum(t.satisfaction for t in tasks if t.status == "completed")
        avg_satisfaction = round(satisfaction_sum / completed_tasks if completed_tasks > 0 else 0, 1)
        
        # 计算时间效率
        planned_seconds = sum(parse_duration(t.planned_time) for t in tasks if t.status == "completed")
        actual_seconds = sum(parse_duration(t.task_len) for t in tasks if t.status == "completed")
        time_efficiency = round((planned_seconds / actual_seconds * 100) if actual_seconds > 0 else 0, 1)
        
        # 计算待办事项完成率
        completion_rate = round((completed_todos / total_todos * 100) if total_todos > 0 else 0, 1)
        
        return {
            "completed_tasks": completed_tasks,
            "total_tasks": total_tasks,
            "completed_todos": completed_todos,
            "total_todos": total_todos,
            "avg_satisfaction": avg_satisfaction,
            "completion_rate": completion_rate,
            "time_efficiency": time_efficiency,
            "planned_time": planned_seconds // 60,  # 转换为分钟
            "actual_time": actual_seconds // 60,    # 转换为分钟
        }

    def show_summary(self):
        """显示今日总结"""
        data = self.get_summary_data()
        
        table = Table(title="今日总结", title_style="bold blue", show_lines=True)
        
        # 添加列
        table.add_column("指标", style="cyan")
        table.add_column("数值", style="magenta")
        
        # 添加数据行
        table.add_row("总任务数", f"{data['total_tasks']}")
        table.add_row("已完成任务", f"{data['completed_tasks']}/{data['total_tasks']} ({data['completion_rate']}%)")
        table.add_row("平均满意度", f"{data['avg_satisfaction']}⭐")
        table.add_row("计划总时长", f"{data['planned_time']//60}h{data['planned_time']%60}m")
        table.add_row("实际总时长", f"{data['actual_time']//60}h{data['actual_time']%60}m")
        table.add_row("时间效率比", f"{data['time_efficiency']}%")
        table.add_row("待办完成率", f"{data['completed_todos']}/{data['total_todos']} ({data['completion_rate']}%)")
        
        console.print(table) 