"""
JSON工具模块
处理JSON文件的读写操作
"""
import json
from pathlib import Path
from typing import Dict, Any

class JsonOp:
    @staticmethod
    def static_method_read_from_json(filepath: str) -> Dict[str, Any]:
        """从JSON文件读取数据"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    @staticmethod
    def static_method_save_to_json(filepath: str, data: Dict[str, Any]) -> None:
        """保存数据到JSON文件"""
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False) 