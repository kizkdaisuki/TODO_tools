"""配置管理模块"""
import os
from pathlib import Path
from prompt_toolkit.styles import Style

class Config:
    # 文件路径相关
    FILEPATH_ROOT = ''
    NOW_TASK_FILEPATH = ''
    COUNT_FILEPATH = ''
    TASKS_JSON = ''
    TASKS_MD = ''
    TODO_JSON = ''
    MEMO_PATH = ''

    # 计数器
    TASK_COUNT = -1

    # 显示相关
    DICT_IMPORTANCE = {
        'low': '🎖', 
        'mid': '️🎖 🎖️ 🎖️', 
        'high': '🎖️ 🎖️ 🎖️ 🎖️ 🎖️'
    }

    DICT_SATISFACTION = {
        1: '🌟', 
        2: '🌟' * 2, 
        3: '🌟' * 3, 
        4: '🌟' * 4, 
        5: '🌟' * 5
    }

    # 时间选项
    TIME_CHOICES = ["25min", "45min", "1h", "1h30min", "2h", "自定义"]

    # 交互式选择的样式
    QUESTIONARY_STYLE = Style([
        ('highlighted', 'bg:#ffffff #000000'),  # 选中项的样式
        ('selected', 'bg:#ffffff #000000 bold'),  # 确认选择后的样式
        ('answer', 'fg:#000000 bg:#ffffff bold'),  # 答案的样式
        ('question', 'bold'),  # 问题的样式
    ])

config = Config() 