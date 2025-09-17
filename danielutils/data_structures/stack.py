import logging
from typing import Optional, Generator, TypeVar, Generic
from .graph import Node
from ..logging_.utils import get_logger
logger = get_logger(__name__)

T = TypeVar('T')


class Stack(Generic[T]):
    """A classic Stack class
    """

    def __init__(self) -> None:
        self.head: Optional[Node[T]] = None
        self.size = 0
        logger.debug("Stack initialized")

    def push(self, value: T):
        """push an item to the stack

        Args:
            value (Any): item to push
        """
        logger.debug(f"Pushing value to stack: {value}")
        if self.head is None:
            self.head = Node(value)
            logger.debug("Created first node in stack")
        else:
            new_head = Node(value, self.head)
            self.head = new_head
            logger.debug("Added new head node to stack")
        self.size += 1
        logger.debug(f"Stack size is now: {self.size}")

    def pop(self) -> T:
        """pop an item from the stack

        Returns:
            Any: poped item
        """
        if not self.is_empty():
            res = self.head.data  # type:ignore
            self.size -= 1
            self.head = self.head.next  # type:ignore
            logger.debug(f"Popped value from stack: {res}, remaining size: {self.size}")
            return res
        logger.warning("Attempted to pop from empty stack")
        raise RuntimeError("Can't pop from an empty stack")

    def peek(self) -> Optional[T]:
        """
        Returns the top element of the stack
        Returns:
            Optional[T]
        """
        if self.is_empty():
            logger.debug("Peek called on empty stack")
            return None
        result = self.head.data  # type:ignore
        logger.debug(f"Peeked at stack top: {result}")
        return result

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
