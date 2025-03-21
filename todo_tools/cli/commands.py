"""
命令行入口
"""
import sys
from todo_tools.core.task_manager import TaskManager
from todo_tools.core.todo_manager import TodoManager
from todo_tools.core.file_manager import init_filepath
from todo_tools.cli.messages import func_print_help_message
import questionary
from todo_tools.utils.config import config

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
        # 选择删除类型
        delete_type = questionary.select(
            "请选择要删除的内容:",
            choices=["待办事项", "已完成任务"],
            style=config.QUESTIONARY_STYLE
        ).ask()
        
        if delete_type == "待办事项":
            task_manager.todo_manager.delete_todo()
        else:
            task_manager.delete_task()
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
    elif cmd == 'show':
        from todo_tools.web.web_server import start_server
        start_server()
    elif cmd == 'dev':
        # 开发模式，启用所有调试功能
        from todo_tools.web.web_server import app
        app.config['DEBUG'] = True
        app.config['TEMPLATES_AUTO_RELOAD'] = True
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=True)
    elif cmd in ['--help', '-h']:
        func_print_help_message()
    else:
        func_print_help_message() 