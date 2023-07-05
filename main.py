import sys
import datetime


def func_save_to_file(func_param_filepath: str):
    with open('file.txt', 'w') as file:
        file.write(func_param_filepath)


def fund_cal_time(func_param_str: str) -> str:
    local_var_time_list = func_param_str.split(':')
    local_var_time_h = int(local_var_time_list[0])
    local_var_time_min = int(local_var_time_list[1])
    local_var_time_sec = int(local_var_time_list[2])
    local_var_end_time = datetime.datetime.now() + datetime.timedelta(hours=local_var_time_h, minutes=local_var_time_min, seconds=local_var_time_sec)
    local_var_end_time = local_var_end_time.time
    return str(local_var_end_time)


def func_init(func_param_args: list):
    local_var_todo = func_param_args[0]
    local_var_cmd = func_param_args[1]
    local_var_time = func_param_args[2]
    local_var_start_time = str(datetime.datetime.now())
    local_var_end_time = fund_cal_time(local_var_time)
    local_val_str = f'{local_var_start_time} ~ {local_var_end_time} {local_var_todo}'
    print(local_val_str)


def func_main(func_param_args: list):
    func_init(func_param_args)


if __name__ == '__main__':
    func_main(sys.argv[1:])
