import sys
import datetime
import re
import os
from functools import singledispatch
from itertools import pairwise
from clock.tomato import clock as tomato_func_clock
from init.init import func_read_json as init_func_read_json
from init.init import func_write_json as init_func_write_json
from voice import func_say as voice_func_say
from message import func_print_hellp_message as message_func_print_hellp_message

GLOBAL_VAR_FILEPATH_ROOT = ''
GLOBAL_VAR_NOW_TASK_FILEPATH = ''
GLOBAL_VAR_COUNT = -1
GLOBAL_VAR_COUNT_FILEPATH = ''
GLOBAL_VAR_DICT_IMPORTANCE = {'low': '🎖', 'mid': '️🎖 🎖️ 🎖️', 'high': '🎖️ 🎖️ 🎖️ 🎖️ 🎖️'}
GLOBAL_VAR_DICT_SATISFACTION = {1: '🌟', 2: '🌟' * 2, 3: '🌟' * 3, '4': '🌟' * 4, 5: '🌟' * 5}

GLOBAL_VAR_JSON_INIT = {}


def func_save_to_file(func_param_filepath: str, func_param_file_content: str = ''):
    global GLOBAL_VAR_COUNT
    if not len(func_param_file_content):
        return
    with open(func_param_filepath, 'a+') as file:
        GLOBAL_VAR_COUNT += 1
        file.write(func_param_file_content)
        file.close()
    with open(GLOBAL_VAR_COUNT_FILEPATH, 'w') as file:
        file.write(str(GLOBAL_VAR_COUNT))
        file.close()


def func_view_file(func_param_filepath: str):
    with open(func_param_filepath, 'r') as file:
        print(file.read())
        file.close()


def func_cal_minutes(func_param_h: int, func_param_min: int) -> int:
    return func_param_h * 60 + func_param_min


def func_cal_seconds(fund_param_time_list) -> int:
    return fund_param_time_list[0] * 3600 + fund_param_time_list[1] * 60 + fund_param_time_list[2]


def func_return_time_form(func_param_sec) -> str:
    local_var_hour = func_param_sec // 3600
    local_var_min = (func_param_sec % 3600) // 60
    local_var_sec = func_param_sec % 60
    return f'{local_var_hour}h{local_var_min}m{local_var_sec}s'


def func_start_task(func_param_str: str) -> str:
    local_var_time_list = func_cal_time(func_param_str)
    tomato_func_clock(func_cal_minutes(local_var_time_list[0], local_var_time_list[1]))
    local_var_end_time = datetime.datetime.now()
    return str(local_var_end_time.strftime('%H:%M:%S'))


def func_cal_time(func_param_str: str) -> list:
    local_var_time_h, local_var_time_min, local_var_time_sec = 0, 0, 0
    local_var_flg = True
    if 'h' in func_param_str:
        local_var_time_h = int(re.split('h|min', func_param_str)[0])
        local_var_flg = False
    if 'min' in func_param_str:
        local_var_time_min = int(re.split('h|min', func_param_str)[1 if 'h' in func_param_str else 0])
        local_var_flg = False
    if local_var_flg:
        local_var_time_list = func_param_str.split(':')
        local_var_time_h = int(local_var_time_list[0])
        local_var_time_min = int(local_var_time_list[1])
        local_var_time_sec = int(local_var_time_list[2])
    return [local_var_time_h, local_var_time_min, local_var_time_sec]


def func_check_cur_count() -> int:
    local_var_cur_count = -1
    with open(GLOBAL_VAR_COUNT_FILEPATH, 'r') as file:
        local_var_cur_count = int(file.read())
    return local_var_cur_count


def func_init_filepath():
    global GLOBAL_VAR_NOW_TASK_FILEPATH
    global GLOBAL_VAR_COUNT
    global GLOBAL_VAR_FILEPATH_ROOT
    global GLOBAL_VAR_COUNT_FILEPATH
    local_var_json_dict = init_func_read_json('/Users/mac/kizk/project/py/todolist/todo.json')
    GLOBAL_VAR_FILEPATH_ROOT = local_var_json_dict['fileroot']
    GLOBAL_VAR_COUNT_FILEPATH = GLOBAL_VAR_FILEPATH_ROOT + 'count.in'
    local_var_now_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    local_var_time_list = local_var_now_time.split('-')
    local_var_filename_year = GLOBAL_VAR_FILEPATH_ROOT + local_var_time_list[0] + '/'
    if not os.path.exists(local_var_filename_year):
        os.makedirs(local_var_filename_year)
    local_var_filename_month = local_var_filename_year + '/' + local_var_time_list[1] + '/'
    if not os.path.exists(local_var_filename_month):
        os.makedirs(local_var_filename_month)
    local_var_filename_day = local_var_filename_month + '/' + local_var_now_time + '.txt'
    GLOBAL_VAR_NOW_TASK_FILEPATH = str(local_var_filename_day)
    if not os.path.exists(local_var_filename_day):
        GLOBAL_VAR_COUNT = 1
    if GLOBAL_VAR_COUNT == -1:
        GLOBAL_VAR_COUNT = func_check_cur_count()


def func_change_task_file_content(func_param_is_vim: bool = True):
    global GLOBAL_VAR_COUNT
    if func_param_is_vim:
        os.system(f'vim {GLOBAL_VAR_NOW_TASK_FILEPATH}')
    with open(GLOBAL_VAR_NOW_TASK_FILEPATH, 'r+') as file:
        local_var_old_file_str = []
        local_var_idx = 1
        for line in file.readlines():
            if line.find('🎖') != -1 and line.find('.') != -1:
                idx = line.find('.')
                line = str(local_var_idx) + line[idx:]
                local_var_idx += 1
            local_var_old_file_str.append(line)
        with open(GLOBAL_VAR_COUNT_FILEPATH, 'w') as f:
            f.write(str(local_var_idx))
            GLOBAL_VAR_COUNT = local_var_idx
            f.close()
        file.close()
    with open(GLOBAL_VAR_NOW_TASK_FILEPATH, 'w') as file:
        file.write(''.join(local_var_old_file_str))
        file.close()


def func_start_clock(func_param_time: str):
    local_var_time_list = func_cal_time(func_param_time)
    local_var_time_h, local_var_time_min, local_var_time_sec = local_var_time_list
    tomato_func_clock(func_cal_minutes(local_var_time_h, local_var_time_min))


def func_init_task_form(func_param_count, func_param_start_time, func_param_end_time, func_param_importance,
                        func_param_todo, func_param_satisfaction) -> str:
    local_var_time_delta = func_cal_seconds(func_cal_time(func_param_end_time)) - func_cal_seconds(
        func_cal_time(func_param_start_time))
    local_var_time_len = func_return_time_form(local_var_time_delta)
    local_var_first = f'{func_param_count}. ︎ ❤️  {local_var_time_len} 💜 {func_param_start_time} ~ {func_param_end_time} {GLOBAL_VAR_DICT_IMPORTANCE[func_param_importance]} \n\n'
    local_var_todo = f'    {func_param_todo} \n \n'
    local_var_summary = f'    summary💬 \n\n'
    local_var_satisfaction = f'    satisfaction ➤ {GLOBAL_VAR_DICT_SATISFACTION[func_param_satisfaction]} \n\n\n'
    local_var_str = local_var_first + local_var_todo + local_var_summary + local_var_satisfaction

    return local_var_str


def func_init(func_param_args: list):
    func_init_filepath()
    func_var_args_length = len(func_param_args)
    if func_var_args_length:
        local_var_cmd = func_param_args[0]
        if local_var_cmd == 'start':
            local_var_todo = func_param_args[1]
            local_var_time = '45min' if len(func_param_args) <= 2 else func_param_args[2]
            local_var_importance = 'mid' if len(func_param_args) <= 3 else func_param_args[3]
            local_var_start_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
            local_var_end_time = func_start_task(local_var_time) # finish clock
            try:
                local_var_satisfaction = int(input('input your satisfaction with 1~5 (default with 3)\n'))
            except ValueError:
                local_var_satisfaction = 3
            except KeyboardInterrupt:
                local_var_satisfaction = 3
            local_var_str = func_init_task_form(GLOBAL_VAR_COUNT, local_var_start_time, local_var_end_time, local_var_importance, local_var_todo, local_var_satisfaction)
            func_save_to_file(GLOBAL_VAR_NOW_TASK_FILEPATH, local_var_str)
            try:
                local_var_summary = input('do you want to add a summary? (y/n) (default with n)\n')
            except ValueError:
                local_var_summary = 'n'
            except KeyboardInterrupt:
                local_var_summary = 'n'
            if local_var_summary == 'y' or local_var_summary == 'Y':
                os.system(f'vim {GLOBAL_VAR_NOW_TASK_FILEPATH}')
        elif local_var_cmd == 'add':
            # TODO

            pass
        elif local_var_cmd == 'list':
            # TODO
            pass
        elif local_var_cmd == 'clock':
            local_var_time = func_param_args[1]
            func_start_clock(local_var_time)
        elif local_var_cmd == '--help' or local_var_cmd == '-h':
            message_func_print_hellp_message()
        elif local_var_cmd == 'modify':
            func_change_task_file_content()
        elif local_var_cmd == 'check':
            func_change_task_file_content(False)
        elif local_var_cmd == 'view':
            func_view_file(GLOBAL_VAR_NOW_TASK_FILEPATH)
    else:
        message_func_print_hellp_message()


def func_main(func_param_args: list):
    func_init(func_param_args)


if __name__ == '__main__':
    func_main(sys.argv[1:])
