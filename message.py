def func_print_hellp_message():
    print()
    print('usage: todo [start] [add] [list] [del] [edit] [clock] [modify] [check] [-h] [--help]')
    print('These are common todo commands used in various situations: ')
    print()
    print('------------------------------------------------------------------')
    print('待办事项管理:')
    print('     ✅ add                    添加待办事项（交互式）')
    print('     ✅ list                   查看待办事项列表')
    print('     ✅ del                    删除待办事项（交互式）')
    print('     ✅ edit                   编辑待办事项（交互式）')
    print()
    print('任务执行:')
    print('     ✅ start                  选择待办事项开始任务')
    print('     ✅ start <任务> <时长> [重要性]  直接开始指定任务')
    print('     ✅ clock <时长>           启动一个计时器')
    print()
    print('任务记录:')
    print('     ✅ view                   查看今日已完成任务')
    print('     ✅ modify                 修改任务记录')
    print('     ✅ check                  检查任务状态')
    print()
    print('其他功能:')
    print('     ✅ memo                   添加备忘录')
    print('     ✅ -h, --help            显示帮助信息')
    print()
    print('时长格式: 25min, 45min, 1h, 1h30min, 2h')
    print('重要性等级: low, mid, high')
    print('------------------------------------------------------------------')
    print()


def func_print_all_message():
    func_print_hellp_message()


def func_main():
    print("start")


if __name__ == '__main__':
    func_main()
