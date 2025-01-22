"""工具模块"""
from . import config
from . import table_utils
from . import time_utils
from . import json_utils

# 导出常用函数
from .json_utils import JsonOp
from .time_utils import (
    func_cal_seconds,
    func_return_time_form,
    func_cal_time,
    parse_duration
) 