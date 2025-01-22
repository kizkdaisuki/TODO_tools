"""
时间工具模块
处理时间相关的功能
"""
import datetime
from dateutil import parser

def func_cal_seconds(func_param_time: str) -> int:
    """计算时间对应的秒数"""
    time_list = func_param_time.split(':')
    return int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int(time_list[2])

def func_return_time_form(func_param_seconds: int) -> str:
    """将秒数转换为时间格式"""
    hours = func_param_seconds // 3600
    minutes = (func_param_seconds % 3600) // 60
    seconds = func_param_seconds % 60
    return f"{hours}h{minutes}m{seconds}s"

def func_cal_time(func_param_time: str) -> str:
    """解析时间字符串"""
    try:
        return datetime.datetime.strptime(func_param_time, '%H:%M:%S').strftime('%H:%M:%S')
    except ValueError:
        return datetime.datetime.now().strftime('%H:%M:%S')

def parse_duration(duration: str) -> int:
    """解析时长字符串为秒数"""
    if 'h' in duration and 'm' in duration:
        hours, minutes = duration.split('h')
        minutes = minutes.replace('min', '').replace('m', '')
        return int(hours) * 3600 + int(minutes) * 60
    elif 'h' in duration:
        hours = duration.replace('h', '')
        return int(hours) * 3600
    elif 'min' in duration or 'm' in duration:
        minutes = duration.replace('min', '').replace('m', '')
        return int(minutes) * 60
    else:
        return 0 