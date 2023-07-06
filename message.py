
def func_print_hellp_message():
    print('usage: todo [-start] [-add] [-list] [-clock]')
    print('These are common todo commands used in various situations: ')
    print('------------------------------------------------------------------')
    print('     ✅ start todo timeduration [importance]')
    print('     ❌ clock ')
    print('     ❌ add todo')
    print('     ❌ list                    show today todo list')
    print('     ✅️ view                    show today start task')
    print('------------------------------------------------------------------')
    print('Example: todo -start English 30min high')


def func_print_all_message():
    func_print_hellp_message()


def func_main():
    print("start")


if __name__ == '__main__':
    func_main()