"""
文件管理器
处理文件路径和文件操作
"""
import os
import datetime
from utils import config
from init.init import func_read_json

def init_filepath():
    """初始化所有文件路径"""
    json_dict = func_read_json('/Users/kizk/kizk/project/py/todolist/todo.json')
    config.FILEPATH_ROOT = json_dict['fileroot']
    config.COUNT_FILEPATH = config.FILEPATH_ROOT + 'count.in'
    
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    time_list = now_time.split('-')
    
    # 创建年份目录
    year_dir = os.path.join(config.FILEPATH_ROOT, time_list[0])
    os.makedirs(year_dir, exist_ok=True)
    
    # 创建月份目录
    month_dir = os.path.join(year_dir, time_list[1])
    os.makedirs(month_dir, exist_ok=True)
    
    # 设置各种文件路径
    config.TASKS_JSON = f'{month_dir}/{now_time}_tasks.json'
    config.TASKS_MD = f'{month_dir}/{now_time}_tasks.md'
    config.TODO_JSON = f'{month_dir}/{now_time}_todo.json'
    config.NOW_TASK_FILEPATH = f'{month_dir}/{now_time}.txt'
    config.MEMO_PATH = f'{month_dir}/{now_time}_memo.txt' 