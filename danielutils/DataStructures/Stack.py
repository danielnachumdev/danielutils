from .Node import Node


class Stack:
    def __init__(self):
        self.head = None
        self.size = 0

    def push(self, value):
        if self.head is None:
            self.head = Node(value)
        else:
            new_head = Node(value, self.head)
            self.head = new_head
        self.size += 1

    def pop(self):
        res = self.head.data
        self.size -= 1
        self.head = self.head.next
        return res

    def __len__(self):
        return self.size

    def __iter__(self):
        while self:
            yield self.pop()

    def is_empty(self):
        return len(self) == 0

    def __bool__(self):
        return not self.is_empty()

    def __contains__(self, value):
        curr = self.head
        while curr is not None:
            if curr.data == value:
                return True
        return False

    def __str__(self):
        values = []
        curr = self.head
        while curr:
            values.append(str(curr.data))
            curr = curr.next
        inside = ", ".join(values)
        return f"Stack({inside})"

    def __repr__(self):
        return str(self)


__all__ = [
    "Stack"
]
