from typing import Generic, TypeVar, Iterator, List as List
from ...reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as List
T = TypeVar("T")


class Queue(Generic[T]):
    """classic Queue data structure"""

    def __init__(self) -> None:
        self.data: list = []

    def pop(self) -> T:
        """return the oldest element while removing it from the queue

        Returns:
            Any: result
        """
        return self.data.pop()

    def push(self, value: T) -> None:
        """adds a new element to the queue

        Args:
            value (Any): the value to add
        """
        self.data.insert(0, value)

    def peek(self) -> T:
        """returns the oldest element in the queue 
        without removing it from the queue

        Returns:
            Any: result
        """
        return self.data[-1]

    def __len__(self) -> int:
        return len(self.data)

    def is_empty(self) -> bool:
        """returns whether the queue is empty

        Returns:
            bool: result
        """
        return len(self) == 0

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return str(self.data)

    def __iter__(self) -> Iterator[T]:
        return iter(self.data)

    def push_many(self, arr: List[T]):
        """will push many objects to the Queue

        Args:
            arr (list): the objects to push
        """
        for v in arr:
            self.push(v)


__all__ = [
    "Queue",
]
