"""
任务模型
定义任务的数据结构和相关方法
"""
from datetime import datetime
from typing import Optional

class Task:
    def __init__(self, 
                 task_id: str,
                 name: str,
                 start_time: str,
                 end_time: str,
                 task_len: str,
                 importance: str,
                 satisfaction: int,
                 status: str = 'completed',
                 summary: str = ''):
        self.task_id = task_id
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.task_len = task_len
        self.importance = importance
        self.satisfaction = satisfaction
        self.status = status
        self.summary = summary
        self.create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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