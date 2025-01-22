"""
待办事项模型
定义待办事项的数据结构和相关方法
"""
class TodoItem:
    def __init__(self, name: str, time: str, importance: str):
        self.name = name
        self.time = time
        self.importance = importance
        self.status = "pending"

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
        todo = TodoItem(data["name"], data["time"], data["importance"])
        todo.status = data.get("status", "pending")
        return todo 