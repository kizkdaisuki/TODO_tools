"""待办事项模型"""
from dataclasses import dataclass

@dataclass
class TodoItem:
    name: str
    time: str
    importance: str
    status: str = "pending"

    def to_dict(self) -> dict:
        """转换为字典格式"""
        return {
            "name": self.name,
            "time": self.time,
            "importance": self.importance,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> 'TodoItem':
        """从字典创建待办事项对象"""
        todo = TodoItem(
            name=data["name"],
            time=data["time"],
            importance=data["importance"]
        )
        todo.status = data.get("status", "pending")
        return todo 