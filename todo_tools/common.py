"""
统一导入管理
所有需要的依赖和工具类都从这里导入
"""
import os
import sys
import json
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

# 第三方库
import questionary
from rich.console import Console
from rich.table import Table
from dateutil import parser

# 工具类
from todo_tools.utils.config import *
from todo_tools.utils.table_utils import console, generate_task_table, generate_todo_table
from todo_tools.utils.time_utils import func_cal_seconds, func_return_time_form, func_cal_time, parse_duration
from todo_tools.utils.json_utils import JsonOp

import os
# 核心功能
# 数据模型
from todo_tools.models.task import Task
from todo_tools.models.todo import TodoItem

# 常用工具函数
def read_json(filepath: str) -> dict:
    """读取JSON文件"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def write_json(filepath: str, data: dict):
    """写入JSON文件"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def ensure_dir(filepath: str):
    """确保目录存在"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True) 