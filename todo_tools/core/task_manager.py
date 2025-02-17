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
from todo_tools.core.day_summary import DaySummary  # 添加这行导入

class TaskManager:
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.load_tasks()
        self.clock = TomatoClock(self)  # 传入 self 以便更新任务状态
        self.todo_manager = TodoManager(self)  # 创建待办事项管理器
        self.day_summary = DaySummary(self, self.todo_manager)  # 创建日总结管理器

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
        
        # 选择模式
        mode = questionary.select(
            "请选择计时模式:",
            choices=["标准模式", "余量模式 (+20%)"],
            default="标准模式",
            style=config.QUESTIONARY_STYLE
        ).ask()
        
        # 创建新任务
        task_id = str(len(self.tasks) + 1)
        start_time = datetime.datetime.now().strftime('%H:%M:%S')
        
        task = Task(
            task_id=task_id,
            name=name,
            start_time=start_time,
            end_time="",
            task_len="",
            planned_time=time_str,  # 保存原始计划时长
            importance=importance,
            satisfaction=0,
            status="running"
        )
        
        # 先保存任务状态
        self.tasks[task_id] = task
        self.save_tasks()
        
        # 计算实际计时时长
        seconds = parse_duration(time_str)
        if mode == "余量模式 (+20%)":
            seconds = int(seconds * 1.2)  # 增加20%的时间
        
        # 启动番茄钟
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

    def show_day_summary(self):
        """显示今日总结"""
        self.day_summary.show_summary()

    def delete_task(self):
        """删除已完成任务"""
        # 只显示已完成的任务
        completed_tasks = {
            k: v for k, v in self.tasks.items() 
            if v.status == "completed"
        }
        
        if not completed_tasks:
            console.print("[yellow]今日暂无已完成任务[/yellow]")
            return

        # 显示任务列表
        table = generate_task_table(completed_tasks)
        console.print(table)

        # 选择要删除的任务
        choices = [
            f"{task_id}: {task.name} ({task.task_len}, {config.DICT_IMPORTANCE[task.importance]})"
            for task_id, task in completed_tasks.items()
        ]

        selected = questionary.select(
            "请选择要删除的任务:",
            choices=choices,
            style=config.QUESTIONARY_STYLE
        ).ask()

        if selected:
            task_id = selected.split(":")[0]
            # 二次确认
            if questionary.confirm(f"确定要删除任务 {task_id}?").ask():
                del self.tasks[task_id]
                self.save_tasks()
                console.print("[green]成功删除任务[/green]")
                self.view_tasks()

    def continue_task(self, task_name: str):
        """继续完成已存在的任务"""
        # 查找最近一次完成的同名任务
        target_task = None
        for task in reversed(self.tasks.values()):
            if task.name == task_name and task.status == "completed":
                target_task = task
                break
        
        if target_task:
            # 选择模式
            mode = questionary.select(
                "请选择计时模式:",
                choices=["标准模式", "余量模式 (+20%)"],
                default="标准模式",
                style=config.QUESTIONARY_STYLE
            ).ask()
            
            # 更新开始时间
            start_time = datetime.datetime.now().strftime('%H:%M:%S')
            
            # 创建新的任务记录（使用新的task_id）
            new_task_id = str(len(self.tasks) + 1)
            task = Task(
                task_id=new_task_id,  # 使用新的task_id
                name=target_task.name,
                start_time=start_time,
                end_time="",
                task_len="",  # 新任务的时长初始为空
                planned_time="45min",  # 新增时长默认45分钟
                importance=target_task.importance,
                satisfaction=target_task.satisfaction,
                status="running"
            )
            
            # 保存新任务状态
            self.tasks[new_task_id] = task  # 使用新的task_id保存
            self.save_tasks()
            
            # 计算番茄钟时长
            seconds = 45 * 60  # 默认45分钟
            if mode == "余量模式 (+20%)":
                seconds = int(seconds * 1.2)  # 增加20%的时间
            
            # 启动番茄钟
            try:
                self.clock.start(task, seconds)
                
                # 番茄钟结束后，更新任务状态
                task.status = "completed"
                self.save_tasks()
                console.print(f"[green]已完成任务 {task_name}[/green]")
                
            except KeyboardInterrupt:
                # 处理中断
                task.status = "completed"
                self.save_tasks()
        else:
            # 如果没有找到历史任务，则创建新任务
            self.start_task([task_name, "45min", "mid"])