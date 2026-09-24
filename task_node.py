class TaskNode:
    def __init__(self, task_id, title, completed=False, next_node=None):
        self.task_id = task_id
        self.title = title
        self.completed = completed
        self.next_node = next_node

    def to_dict(self):
        return {
            "id": self.task_id,
            "title": self.title,
            "completed": self.completed,
        }
