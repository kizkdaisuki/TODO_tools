"""
全局配置和常量
包含所有全局变量和配置项
"""
import os

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