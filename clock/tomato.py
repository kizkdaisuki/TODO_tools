#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Pomodoro 番茄工作法 https://en.wikipedia.org/wiki/Pomodoro_Technique
# ====== 🍅 Tomato Clock =======
# ./tomato.py         # start a 25 minutes tomato clock + 5 minutes break
# ./tomato.py -t      # start a 25 minutes tomato clock
# ./tomato.py -t <n>  # start a <n> minutes tomato clock
# ./tomato.py -b      # take a 5 minutes break
# ./tomato.py -b <n>  # take a <n> minutes break
# ./tomato.py -h      # help


import sys
import time
import subprocess
import datetime

WORK_MINUTES = 25
BREAK_MINUTES = 5


def main():
    try:
        if len(sys.argv) <= 1:
            print(f'🍅 tomato {WORK_MINUTES} minutes. Ctrl+C to exit')
            tomato(WORK_MINUTES, 'It is time to take a break')
            print(f'🛀 break {BREAK_MINUTES} minutes. Ctrl+C to exit')
            tomato(BREAK_MINUTES, 'It is time to work')

        elif sys.argv[1] == '-t':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
            print(f'🍅 tomato {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to take a break')

        elif sys.argv[1] == '-b':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
            print(f'🛀 break {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to work')

        elif sys.argv[1] == '-h':
            help()

        else:
            help()

    except KeyboardInterrupt:
        print('\n👋 goodbye')
    except Exception as ex:
        print(ex)
        exit(1)


def clock(minutes, notify_msg='ご主人様、お仕事疲れ様でした') -> None:
    h, m = minutes // 60, minutes % 60
    start_time = time.perf_counter()
    end_time = datetime.datetime.now() + datetime.timedelta(hours=h, minutes=m)
    end_time = str(end_time.strftime('%H:%M:%S'))
    try:
        while True:
            diff_seconds = int(round(time.perf_counter() - start_time))
            left_seconds = minutes * 60 - diff_seconds
            now_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
            if left_seconds <= 0 and now_time == end_time:
                print('')
                break

            countdown = '{}:{} ⏰'.format(int(left_seconds / 60), int(left_seconds % 60))
            duration = min(minutes, 25)
            progressbar(diff_seconds, minutes * 60, duration, countdown)
            time.sleep(1)
    except KeyboardInterrupt:
        print('\n👋 goodbye')
    finally:
        notify_me(notify_msg)


def tomato(minutes, notify_msg):
    start_time = time.perf_counter()
    sec_cnt = 0
    while True:
        diff_seconds = int(round(time.perf_counter() - start_time))
        left_seconds = minutes * 60 - diff_seconds
        if left_seconds <= 0:
            print('')
            break

        countdown = '{}:{} ⏰'.format(int(left_seconds / 60), int(left_seconds % 60))
        duration = min(minutes, 25)
        progressbar(diff_seconds, minutes * 60, duration, countdown)
        time.sleep(1)
        sec_cnt += 1
    notify_me(notify_msg)


def progressbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')


def send_notification(title, message, subtitle=None, sound=None, activate=None):
    # 构建AppleScript命令
    script = f'display notification "{message}" with title "{title}"'
    if subtitle:
        script += f' subtitle "{subtitle}"'
    if sound:
        script += f' sound name "{sound}"'
    if activate:
        script += f' activate "{activate}"'

    # 使用osascript运行AppleScript命令
    subprocess.run(['osascript', '-e', script])
def notify_me(msg):
    is_say_flg = False # 默认为提醒声音关闭
    print(msg)
    try:
        if sys.platform == 'darwin': # macos
            # macos desktop notification
            try:
                # subprocess.run(['terminal-notifier', '-title', '🍅', '-message', msg])
                title = '🍅'
                message = msg
                subtitle = 'sub'
                sound = 'Frog'
                send_notification(
                    title=title,
                    message=message,
                    subtitle=subtitle,
                    sound=sound,
                )
                subprocess.run(['say', '-v', 'Kyoko', msg])
            except Exception as e:
                print('macos error:', e)

            if is_say_flg:
                subprocess.run(['say', '-v', 'Kyoko', msg])
        elif sys.platform.startswith('linux'): # linux
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", '🍅', msg])
        else:  # windows?
            # TODO: windows notification
            pass

    except:
        # skip the notification error
        pass


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith('.py') else 'tomato'  # tomato is pypi package
    print('====== 🍅 Tomato Clock =======')
    print(f'{appname}         # start a {WORK_MINUTES} minutes tomato clock + {BREAK_MINUTES} minutes break')
    print(f'{appname} -t      # start a {WORK_MINUTES} minutes tomato clock')
    print(f'{appname} -t <n>  # start a <n> minutes tomato clock')
    print(f'{appname} -b      # take a {BREAK_MINUTES} minutes break')
    print(f'{appname} -b <n>  # take a <n> minutes break')
    print(f'{appname} -h      # help')


if __name__ == "__main__":
    main()
