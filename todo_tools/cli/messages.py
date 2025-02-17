"""命令行提示信息"""
from rich.console import Console

console = Console()

def func_print_help_message():
    """显示帮助信息"""
    console.print()
    console.print('usage: todo [start] [add] [list] [del] [edit] [view] [-h] [--help]')
    console.print('These are common todo commands used in various situations: ')
    console.print()
    console.print('------------------------------------------------------------------')
    console.print('待办事项管理:')
    console.print('     ✅ add                    添加待办事项（交互式）')
    console.print('     ✅ add <任务名称>          快速添加待办事项（默认45min, mid）')
    console.print('     ✅ list                   查看待办事项列表')
    console.print('     ✅ del                    删除待办事项或已完成任务（交互式）')
    console.print('     ✅ edit                   编辑待办事项（交互式）')
    console.print()
    console.print('任务执行:')
    console.print('     ✅ start                  选择待办事项开始任务')
    console.print('     ✅ start <任务名称>        直接开始任务（默认45min, mid）')
    console.print('     ✅ start <任务名称> <时长>  指定时长开始任务（默认mid）')
    console.print('     ✅ start <任务名称> <时长> <重要性>  完整参数开始任务')
    console.print()
    console.print('任务记录:')
    console.print('     ✅ view                   查看今日已完成任务')
    console.print('     ✅ modify                 修改任务记录（交互式）')
    console.print('     ✅ day                    查看今日任务总结')
    console.print('     ✅ -h, --help            显示帮助信息')
    console.print()
    console.print('时长格式: 25min, 45min, 1h, 1h30min, 2h')
    console.print('重要性等级: low, mid, high')
    console.print('------------------------------------------------------------------')
    console.print('可视化:')
    console.print('     ✅ show                   在浏览器中查看可视化面板')
    console.print() 