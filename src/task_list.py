from task_node import TaskNode


class TaskList:
    def __init__(self):
        self.head = None
        self._next_id = 1

    def append(self, title):
        node = TaskNode(self._next_id, title)
        self._next_id += 1
        if self.head is None:
            self.head = node
            return node
        current = self.head
        while current.next_node is not None:
            current = current.next_node
        current.next_node = node
        return node

    def find(self, task_id):
        current = self.head
        while current is not None:
            if current.task_id == task_id:
                return current
            current = current.next_node
        return None

    def update(self, task_id, title):
        node = self.find(task_id)
        if node is None:
            return None
        node.title = title
        return node

    def toggle(self, task_id):
        node = self.find(task_id)
        if node is None:
            return None
        node.completed = not node.completed
        return node

    def remove(self, task_id):
        previous = None
        current = self.head
        while current is not None:
            if current.task_id == task_id:
                if previous is None:
                    self.head = current.next_node
                else:
                    previous.next_node = current.next_node
                return True
            previous = current
            current = current.next_node
        return False

    def to_list(self):
        items = []
        current = self.head
        while current is not None:
            items.append(current.to_dict())
            current = current.next_node
        return items
