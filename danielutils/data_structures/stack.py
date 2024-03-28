from typing import Optional, Generator, Any, cast
from .graph import Node


class Stack:
    """A classic Stack class
    """

    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.size = 0

    def push(self, value: Any):
        """push an item to the stack

        Args:
            value (Any): item to push
        """
        if self.head is None:
            self.head = Node(value)
        else:
            new_head = Node(value, self.head)
            self.head = new_head
        self.size += 1

    def pop(self) -> Any:
        """pop an item from the stack

        Returns:
            Any: poped item
        """
        if not self.is_empty():
            self.head = cast(Node, self.head)
            res = self.head.data
            self.size -= 1
            self.head = self.head.next
            return res

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Generator:
        while self:
            yield self.pop()

    def is_empty(self) -> bool:
        """return whether the stack is empty
        """
        return len(self) == 0

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __contains__(self, value) -> bool:
        curr = self.head
        while curr is not None:
            if curr.data == value:
                return True
        return False

    def __str__(self) -> str:
        values = []
        curr = self.head
        while curr:
            values.append(str(curr.data))
            curr = curr.next
        inside = ", ".join(values)
        return f"Stack({inside})"

    def __repr__(self) -> str:
        return str(self)


__all__ = [
    "Stack"
]
