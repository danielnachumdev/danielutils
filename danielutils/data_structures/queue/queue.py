import logging
from typing import Generic, TypeVar, Iterator, List as List
from ...reflection import get_python_version
from ...logging_.utils import get_logger

if get_python_version() >= (3, 9):
    from builtins import list as List
T = TypeVar("T")

logger = get_logger(__name__)


class Queue(Generic[T]):
    """classic Queue data structure"""

    def __init__(self) -> None:
        self.data: list = []
        logger.debug("Queue initialized")

    def pop(self) -> T:
        """return the oldest element while removing it from the queue

        Returns:
            Any: result
        """
        if self.is_empty():
            logger.warning("Attempted to pop from empty queue")
            raise IndexError("pop from empty queue")
        
        result = self.data.pop()
        logger.debug("Popped element from queue, remaining size: %s", len(self.data))
        return result

    def push(self, value: T) -> None:
        """adds a new element to the queue

        Args:
            value (Any): the value to add
        """
        self.data.insert(0, value)
        logger.debug("Pushed element to queue, new size: %s", len(self.data))

    def peek(self) -> T:
        """returns the oldest element in the queue 
        without removing it from the queue

        Returns:
            Any: result
        """
        if self.is_empty():
            logger.warning("Attempted to peek at empty queue")
            raise IndexError("peek at empty queue")
        
        result = self.data[-1]
        logger.debug("Peeked at element in queue, size: %s", len(self.data))
        return result

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
        logger.debug("Pushing %s elements to queue", len(arr))
        for v in arr:
            self.push(v)
        logger.info("Successfully pushed %s elements to queue", len(arr))


__all__ = [
    "Queue",
]
