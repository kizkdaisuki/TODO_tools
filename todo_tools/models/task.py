"""任务模型"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    task_id: str
    name: str
    start_time: str
    end_time: str
    task_len: str
    importance: str
    satisfaction: int
    status: str = 'completed'
    summary: str = ''
    create_time: str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            'task_id': self.task_id,
            'task_name': self.name,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'task_len': self.task_len,
            'importance': self.importance,
            'satisfaction': self.satisfaction,
            'status': self.status,
            'summary': self.summary,
            'create_time': self.create_time
        }

    @staticmethod
    def from_dict(data: dict) -> 'Task':
        """从字典创建任务对象"""
        return Task(
            task_id=str(data['task_id']),
            name=data['task_name'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            task_len=data['task_len'],
            importance=data['importance'],
            satisfaction=data['satisfaction'],
            status=data.get('status', 'completed'),
            summary=data.get('summary', '')
        ) 