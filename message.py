
def func_print_hellp_message():
    print()
    print('usage: todo [start] [add] [list] [clock] [modify] [-h] [--help]')
    print('These are common todo commands used in various situations: ')
    print()
    print('------------------------------------------------------------------')
    print('     ✅ start todo timeduration [importance]          start task')
    print('     ✅️ clock time              start a clock')
    print('     ❌ add todo')
    print('     ❌ list                    show today todo list')
    print('     ✅️ view                    show today start tasks')
    print('     ✅️ modify                  modify the start tasks')
    print('------------------------------------------------------------------')
    print('Example: todo -start English 30min high')
    print('Example: clock 00:15:00')
    print('Example: clock 1h30min')


def func_print_all_message():
    func_print_hellp_message()


def func_main():
    print("start")


if __name__ == '__main__':
    func_main()