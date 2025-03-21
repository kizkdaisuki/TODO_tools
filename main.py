"""
主入口文件
处理命令行参数并调用相应的功能
"""
from todo_tools.common import *
from todo_tools.core.task_manager import TaskManager
from todo_tools.core.todo_manager import TodoManager
from todo_tools.core.file_manager import init_filepath
from todo_tools.cli.messages import func_print_hellp_message

def main(args: list):
    """主函数"""
    # 初始化文件路径
    init_filepath()
    
    if not args:
        func_print_hellp_message()
        return
    
    # 获取命令
    cmd = args[0]
    
    # 任务管理器
    task_manager = TaskManager()
    # 待办事项管理器
    todo_manager = TodoManager()
    
    # 命令处理
    if cmd == 'start':
        if len(args) == 1:
            todo_manager.start_from_todo()
        else:
            task_manager.start_task(args[1:])
    elif cmd == 'add':
        todo_manager.add_todo()
    elif cmd == 'list':
        todo_manager.list_todos()
    elif cmd == 'del':
        todo_manager.delete_todo()
    elif cmd == 'edit':
        todo_manager.edit_todo()
    elif cmd == 'view':
        task_manager.view_tasks()
    elif cmd == 'modify':
        task_manager.modify_tasks()
    elif cmd == 'check':
        task_manager.check_tasks()
    elif cmd in ['--help', '-h']:
        func_print_hellp_message()
    else:
        func_print_hellp_message()

if __name__ == '__main__':
    main(sys.argv[1:])
