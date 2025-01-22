"""任务管理器"""
from typing import List, Dict
import datetime
from todo_tools.models.task import Task
from todo_tools.utils.json_utils import JsonOp
from todo_tools.utils.table_utils import generate_task_table, console, generate_timer_table
from todo_tools.utils.config import config
from todo_tools.utils.time_utils import parse_duration
from todo_tools.core.clock import TomatoClock
from todo_tools.core.todo_manager import TodoManager
import questionary

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.load_tasks()
        self.clock = TomatoClock(self)  # 传入 self 以便更新任务状态
        self.todo_manager = TodoManager(self)  # 创建待办事项管理器

    def load_tasks(self):
        """加载任务"""
        data = JsonOp.static_method_read_from_json(config.TASKS_JSON)
        self.tasks = {k: Task.from_dict(v) for k, v in data.items()}

    def save_tasks(self):
        """保存任务"""
        data = {k: task.to_dict() for k, task in self.tasks.items()}
        JsonOp.static_method_save_to_json(config.TASKS_JSON, data)

    def view_tasks(self):
        """查看任务"""
        # 只显示已完成的任务
        completed_tasks = {
            k: v for k, v in self.tasks.items() 
            if v.status == "completed"
        }
        
        if not completed_tasks:
            console.print("[yellow]今日暂无任务记录[/yellow]")
            return
        table = generate_task_table(completed_tasks)
        console.print(table)

    def start_task(self, args: List[str]):
        """开始一个新任务"""
        if not args:
            console.print("[red]请提供任务名称[/red]")
            return
        
        name = args[0]
        time_str = args[1] if len(args) > 1 else "45min"  # 默认45分钟
        importance = args[2] if len(args) > 2 else "mid"  # 默认中等重要性
        
        # 创建新任务
        task_id = str(len(self.tasks) + 1)
        start_time = datetime.datetime.now().strftime('%H:%M:%S')
        
        task = Task(
            task_id=task_id,
            name=name,
            start_time=start_time,
            end_time="",
            task_len=time_str,
            importance=importance,
            satisfaction=0,
            status="running"
        )
        
        # 先保存任务状态
        self.tasks[task_id] = task
        self.save_tasks()
        
        # 启动番茄钟
        seconds = parse_duration(time_str)
        try:
            self.clock.start(task, seconds)
        except KeyboardInterrupt:
            task.status = "completed"
            self.save_tasks()

    def save_task(self, task: Task):
        """保存单个任务"""
        self.tasks[task.task_id] = task
        self.save_tasks()

    def modify_tasks(self):
        """修改任务记录"""
        if not self.tasks:
            console.print("[yellow]今日暂无任务记录[/yellow]")
            return

        # 显示任务列表
        self.view_tasks()

        # 选择要修改的任务
        choices = [
            f"{task_id}: {task.name} ({task.task_len}, {config.DICT_IMPORTANCE[task.importance]})"
            for task_id, task in self.tasks.items()
            if task.status == "completed"
        ]

        if not choices:
            console.print("[yellow]没有可修改的任务[/yellow]")
            return

        selected = questionary.select(
            "请选择要修改的任务:",
            choices=choices,
            style=config.QUESTIONARY_STYLE
        ).ask()

        if selected:
            task_id = selected.split(":")[0]
            task = self.tasks[task_id]

            # 选择要修改的字段
            field = questionary.select(
                "请选择要修改的内容:",
                choices=["任务名称", "时长", "重要性", "满意度", "总结"],
                style=config.QUESTIONARY_STYLE
            ).ask()

            if field == "任务名称":
                new_name = questionary.text(
                    "请输入新的任务名称:",
                    default=task.name
                ).ask()
                if new_name:
                    task.name = new_name
            elif field == "时长":
                new_time = questionary.select(
                    "请选择新的时长:",
                    choices=config.TIME_CHOICES,
                    default=task.task_len,
                    style=config.QUESTIONARY_STYLE
                ).ask()
                if new_time == "自定义":
                    new_time = questionary.text(
                        "请输入时长 (例如: 1h30min):",
                        default=task.task_len
                    ).ask()
                if new_time:
                    task.task_len = new_time
            elif field == "重要性":
                new_importance = questionary.select(
                    "请选择新的重要性:",
                    choices=["low", "mid", "high"],
                    default=task.importance,
                    style=config.QUESTIONARY_STYLE
                ).ask()
                if new_importance:
                    task.importance = new_importance
            elif field == "满意度":
                while True:
                    satisfaction = questionary.text(
                        "请输入新的满意度评分 (1-5):",
                        default=str(task.satisfaction)
                    ).ask()
                    try:
                        score = int(satisfaction)
                        if 1 <= score <= 5:
                            task.satisfaction = score
                            break
                        else:
                            console.print("[red]请输入1-5之间的数字[/red]")
                    except ValueError:
                        console.print("[red]请输入有效的数字[/red]")
            elif field == "总结":
                new_summary = questionary.text(
                    "请输入新的任务总结:",
                    default=task.summary
                ).ask()
                if new_summary:
                    task.summary = new_summary

            self.save_tasks()
            console.print("[green]成功更新任务[/green]")
            self.view_tasks()