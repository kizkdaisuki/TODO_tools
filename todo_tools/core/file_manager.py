"""
文件管理器
处理文件路径和文件操作
"""
import os
import datetime
from pathlib import Path
from todo_tools.utils.json_utils import JsonOp
from todo_tools.utils.config import config

def init_filepath():
    """初始化所有文件路径"""
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # 读取配置文件
    config_path = os.path.join(project_root, 'todo.json')
    if not os.path.exists(config_path):
        # 如果配置文件不存在，创建默认配置
        default_data_dir = os.path.join(project_root, 'data')
        config_data = {'fileroot': default_data_dir}
        JsonOp.static_method_save_to_json(config_path, config_data)
    else:
        config_data = JsonOp.static_method_read_from_json(config_path)
    
    # 设置根目录
    root_dir = config_data.get('fileroot')
    if not root_dir:
        root_dir = os.path.join(project_root, 'data')
    
    # 确保目录存在
    os.makedirs(root_dir, exist_ok=True)
    
    # 更新配置
    config.FILEPATH_ROOT = root_dir
    
    # 获取当前日期
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')
    year, month, _ = now_time.split('-')
    
    # 创建年份目录
    year_dir = os.path.join(root_dir, year)
    os.makedirs(year_dir, exist_ok=True)
    
    # 创建月份目录
    month_dir = os.path.join(year_dir, month)
    os.makedirs(month_dir, exist_ok=True)
    
    # 设置各种文件路径
    config.COUNT_FILEPATH = os.path.join(root_dir, 'count.in')
    config.TASKS_JSON = os.path.join(month_dir, f'{now_time}_tasks.json')
    config.TASKS_MD = os.path.join(month_dir, f'{now_time}_tasks.md')
    config.TODO_JSON = os.path.join(month_dir, f'{now_time}_todo.json')
    config.NOW_TASK_FILEPATH = os.path.join(month_dir, f'{now_time}.txt')
    config.MEMO_PATH = os.path.join(month_dir, f'{now_time}_memo.txt') 