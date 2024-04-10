from typing import Optional, Generator, Any, cast, TypeVar, Generic
from .graph import Node

T = TypeVar('T')


class Stack(Generic[T]):
    """A classic Stack class
    """

    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.size = 0

    def push(self, value: T):
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

    def pop(self) -> T:
        """pop an item from the stack

        Returns:
            Any: poped item
        """
        if not self.is_empty():
            res = self.head.data
            self.size -= 1
            self.head = self.head.next
            return res

    def __len__(self) -> int:
        return self.size

    def __iter__(self) -> Generator[T, None, None]:
        while self:
            yield self.pop()

    def is_empty(self) -> bool:
        """return whether the stack is empty
        """
        return len(self) == 0

    def __bool__(self) -> bool:
        return not self.is_empty()

    def __contains__(self, value: T) -> bool:
        curr = self.head
        while curr is not None:
            if curr.data == value:
                return True
            curr = curr.next
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
