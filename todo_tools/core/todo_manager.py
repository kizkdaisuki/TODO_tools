"""待办事项管理器"""
from typing import Dict, Optional
import questionary
from todo_tools.models.todo import TodoItem
from todo_tools.utils.json_utils import JsonOp
from todo_tools.utils.table_utils import generate_todo_table, console
from todo_tools.utils.config import config

class TodoManager:
    def __init__(self, task_manager):
        self.todos: Dict[str, TodoItem] = {}
        self.task_manager = task_manager
        self.load_todos()

    def load_todos(self):
        """加载待办事项"""
        data = JsonOp.static_method_read_from_json(config.TODO_JSON)
        self.todos = {k: TodoItem.from_dict(v) for k, v in data.items()}

    def save_todos(self):
        """保存待办事项"""
        data = {k: todo.to_dict() for k, todo in self.todos.items()}
        JsonOp.static_method_save_to_json(config.TODO_JSON, data)

    def list_todos(self):
        """显示待办事项列表"""
        if not self.todos:
            console.print("[yellow]当前没有待办事项[/yellow]")
            return
        table = generate_todo_table(self.todos)
        console.print(table)

    def add_todo(self, name: str = None):
        """添加待办事项"""
        # 获取任务名称
        if name is None:  # 交互式添加
            name = questionary.text("请输入任务名称:").ask()
            if not name:
                return
            
            # 选择时长
            time = questionary.select(
                "请选择预计时长:",
                choices=config.TIME_CHOICES,
                default="45min",
                style=config.QUESTIONARY_STYLE
            ).ask()
            
            if time == "自定义":
                time = questionary.text("请输入时长 (例如: 1h30min):").ask()

            # 选择重要性
            importance = questionary.select(
                "请选择重要性:",
                choices=["low", "mid", "high"],
                default="mid",
                style=config.QUESTIONARY_STYLE
            ).ask()
        else:  # 快速添加，使用默认值
            time = "45min"
            importance = "mid"

        # 创建并保存待办事项
        todo_id = str(len(self.todos) + 1)
        self.todos[todo_id] = TodoItem(name, time, importance)
        self.save_todos()

        console.print("[green]成功添加待办事项[/green]")
        self.list_todos()

    def delete_todo(self):
        """删除待办事项"""
        # 只显示未完成的待办事项
        pending_todos = {
            k: v for k, v in self.todos.items() 
            if v.status == "pending"
        }
        
        if not pending_todos:
            console.print("[yellow]当前没有待办事项[/yellow]")
            return

        # 显示待办事项列表
        table = generate_todo_table(pending_todos)
        console.print(table)

        # 选择要删除的项目
        choices = [
            f"{todo_id}: {todo.name} ({todo.time}, {config.DICT_IMPORTANCE[todo.importance]})"
            for todo_id, todo in pending_todos.items()
        ]

        selected = questionary.select(
            "请选择要删除的待办事项:",
            choices=choices,
            style=config.QUESTIONARY_STYLE
        ).ask()

        if selected:
            todo_id = selected.split(":")[0]
            # 二次确认
            if questionary.confirm(f"确定要删除待办事项 {todo_id}?").ask():
                self.todos[todo_id].status = "deleted"
                self.save_todos()
                console.print("[green]成功删除待办事项[/green]")
                self.list_todos()

    def edit_todo(self):
        """编辑待办事项"""
        if not self.todos:
            console.print("[yellow]当前没有待办事项[/yellow]")
            return

        # 显示待办事项列表
        self.list_todos()

        # 选择要编辑的项目
        choices = [
            f"{todo_id}: {todo.name} ({todo.time}, {config.DICT_IMPORTANCE[todo.importance]})"
            for todo_id, todo in self.todos.items()
            if todo.status == "pending"
        ]

        if not choices:
            console.print("[yellow]没有可编辑的待办事项[/yellow]")
            return

        selected = questionary.select(
            "请选择要编辑的待办事项:",
            choices=choices,
            style=config.QUESTIONARY_STYLE
        ).ask()

        if selected:
            todo_id = selected.split(":")[0]
            todo = self.todos[todo_id]

            # 选择要编辑的字段
            field = questionary.select(
                "请选择要编辑的内容:",
                choices=["任务名称", "预计时长", "重要性"],
                style=config.QUESTIONARY_STYLE
            ).ask()

            if field == "任务名称":
                new_name = questionary.text("请输入新的任务名称:", default=todo.name).ask()
                if new_name:
                    todo.name = new_name
            elif field == "预计时长":
                new_time = questionary.select(
                    "请选择新的预计时长:",
                    choices=config.TIME_CHOICES,
                    style=config.QUESTIONARY_STYLE
                ).ask()
                if new_time == "自定义":
                    new_time = questionary.text("请输入时长 (例如: 1h30min):", default=todo.time).ask()
                if new_time:
                    todo.time = new_time
            elif field == "重要性":
                new_importance = questionary.select(
                    "请选择新的重要性:",
                    choices=["low", "mid", "high"],
                    default=todo.importance,
                    style=config.QUESTIONARY_STYLE
                ).ask()
                if new_importance:
                    todo.importance = new_importance

            self.save_todos()
            console.print("[green]成功更新待办事项[/green]")
            self.list_todos()

    def start_from_todo(self):
        """从待办事项开始任务"""
        if not self.todos:
            console.print("[yellow]当前没有待办事项[/yellow]")
            return

        # 显示待办事项列表
        self.list_todos()

        # 选择要开始的项目
        choices = [
            f"{todo_id}: {todo.name} ({todo.time}, {config.DICT_IMPORTANCE[todo.importance]})"
            for todo_id, todo in self.todos.items()
            if todo.status == "pending"
        ]

        if not choices:
            console.print("[yellow]没有可开始的待办事项[/yellow]")
            return

        selected = questionary.select(
            "请选择要开始的待办事项:",
            choices=choices,
            style=config.QUESTIONARY_STYLE
        ).ask()

        if selected:
            todo_id = selected.split(":")[0]
            todo = self.todos[todo_id]
            
            # 标记待办事项为已完成
            todo.status = "completed"
            self.save_todos()
            
            # 启动对应的任务
            self.task_manager.start_task([todo.name, todo.time, todo.importance]) 