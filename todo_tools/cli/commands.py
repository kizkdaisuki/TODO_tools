"""
命令行入口
"""
import sys
from todo_tools.core.task_manager import TaskManager
from todo_tools.core.todo_manager import TodoManager
from todo_tools.core.file_manager import init_filepath
from todo_tools.cli.messages import func_print_help_message

def main():
    """主函数"""
    # 初始化文件路径
    init_filepath()
    
    args = sys.argv[1:]
    if not args:
        func_print_help_message()
        return
    
    # 获取命令
    cmd = args[0]
    
    # 任务管理器
    task_manager = TaskManager()
    
    # 命令处理
    if cmd == 'start':
        if len(args) == 1:
            task_manager.todo_manager.start_from_todo()
        else:
            task_manager.start_task(args[1:])
    elif cmd == 'add':
        if len(args) > 1:
            task_manager.todo_manager.add_todo(args[1])  # 直接添加带名称的待办事项
        else:
            task_manager.todo_manager.add_todo()  # 交互式添加
    elif cmd == 'list':
        task_manager.todo_manager.list_todos()
    elif cmd == 'del':
        task_manager.todo_manager.delete_todo()
    elif cmd == 'edit':
        task_manager.todo_manager.edit_todo()
    elif cmd == 'view':
        task_manager.view_tasks()
    elif cmd == 'modify':
        task_manager.modify_tasks()
    elif cmd == 'check':
        task_manager.check_tasks()
    elif cmd == 'day':
        task_manager.show_day_summary()
    elif cmd in ['--help', '-h']:
        func_print_help_message()
    else:
        func_print_help_message() 