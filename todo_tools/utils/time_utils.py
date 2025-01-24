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
    if not duration:
        return 0
    
    try:
        # 处理时分秒格式 (例如: "0h45m0s")
        hours = minutes = seconds = 0
        
        # 处理小时部分
        if 'h' in duration:
            parts = duration.split('h')
            hours = int(parts[0])
            duration = parts[1] if len(parts) > 1 else ''
        
        # 处理分钟部分
        if 'm' in duration:
            parts = duration.split('m')
            minutes = int(parts[0])
            duration = parts[1] if len(parts) > 1 else ''
        
        # 处理秒数部分
        if 's' in duration:
            seconds = int(duration.rstrip('s'))
        elif duration and duration.isdigit():
            seconds = int(duration)
            
        return hours * 3600 + minutes * 60 + seconds
        
    except (ValueError, IndexError):
        # 如果解析失败，尝试其他格式
        try:
            # 处理纯数字（假设是分钟）
            if duration.isdigit():
                return int(duration) * 60
                
            # 处理分钟格式 (例如: "45min")
            if 'min' in duration:
                minutes = int(duration.replace('min', ''))
                return minutes * 60
                
            # 处理纯秒数格式 (例如: "450s")
            if duration.endswith('s'):
                return int(duration.rstrip('s'))
                
        except (ValueError, IndexError):
            return 0
            
    return 0  # 无法解析的格式返回0 