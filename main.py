import sys
import datetime
import re
import os
from voice import func_say as voice_func_say

GLOBAL_VAR_FILEPATH_ROOT = '/Users/mac/kizk/project/py/todolist/'
GLOBAL_VAR_NOW_FILEPATH = ''
GLOBAL_VAR_COUNT = -1
GLOBAL_VAR_COUNT_FILEPATH = '/Users/mac/kizk/project/py/todolist/count.in'


def func_save_to_file(func_param_filepath: str, func_param_file_content: str = ''):
    global GLOBAL_VAR_COUNT
    if not len(func_param_file_content):
        return
    with open(func_param_filepath, 'a+') as file:
        GLOBAL_VAR_COUNT += 1
        file.write(func_param_file_content)
    with open(GLOBAL_VAR_COUNT_FILEPATH, 'w') as file:
        file.write(str(GLOBAL_VAR_COUNT))


def func_cal_time(func_param_str: str) -> str:
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
    local_var_end_time = datetime.datetime.now() + datetime.timedelta(hours=local_var_time_h, minutes=local_var_time_min, seconds=local_var_time_sec)
    return str(local_var_end_time.strftime('%H:%M:%S'))


def func_init_filepath():
    global GLOBAL_VAR_NOW_FILEPATH
    global GLOBAL_VAR_COUNT
    local_var_now_time = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    local_var_time_list = local_var_now_time.split('-')
    local_var_filename_year = GLOBAL_VAR_FILEPATH_ROOT + local_var_time_list[0] + '/'
    if not os.path.exists(local_var_filename_year):
        os.makedirs(local_var_filename_year)
    local_var_filename_month = local_var_filename_year + '/' + local_var_time_list[1] + '/'
    if not os.path.exists(local_var_filename_month):
        os.makedirs(local_var_filename_month)
    local_var_filename_day = local_var_filename_month + '/' + local_var_now_time + '.txt'
    GLOBAL_VAR_NOW_FILEPATH = str(local_var_filename_day)
    if not os.path.exists(local_var_filename_day):
        GLOBAL_VAR_COUNT = 1
    if GLOBAL_VAR_COUNT == -1:
        with open(GLOBAL_VAR_COUNT_FILEPATH, 'r') as file:
            GLOBAL_VAR_COUNT = int(file.read())
    print(local_var_now_time)


def func_init(func_param_args: list):
    func_init_filepath()
    func_var_args_length = len(func_param_args)
    if func_var_args_length == 1:
        # TODO
        pass
    elif func_var_args_length == 2:
        # TODO
        pass
    elif func_var_args_length == 3:
        local_var_todo = func_param_args[0]
        local_var_cmd = func_param_args[1]
        local_var_time = func_param_args[2]
        local_var_start_time = str(datetime.datetime.now().strftime('%H:%M:%S'))
        local_var_end_time = func_cal_time(local_var_time)
        local_val_str = f'{GLOBAL_VAR_COUNT}. {local_var_start_time} ~ {local_var_end_time} \n {local_var_todo} \n \n'
        func_save_to_file(GLOBAL_VAR_NOW_FILEPATH, local_val_str)


def func_main(func_param_args: list):
    func_init(func_param_args)


if __name__ == '__main__':
    func_main(sys.argv[1:])
