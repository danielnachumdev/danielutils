import logging
from typing import Union, TypeVar, Generic
from ..comparer import Comparer
from ...logging_.utils import get_logger
logger = get_logger(__name__)

T = TypeVar("T")


class Heap(Generic[T]):
    """a Heap class which will do the sorting according to the supplied comparer object
    """

    def __init__(self, comparer: Comparer) -> None:
        logger.debug("Initializing Heap with comparer: %s", type(comparer).__name__)
        self.arr: list = []
        self.comparer = comparer

    def push(self, val: T) -> None:
        """will add a new object to the heap

        Args:
            val (Any): the object to add to the heap
        """
        logger.debug("Pushing value to heap: %s", val)
        res: Union[int, float] = -1
        curr_index = len(self)
        self.arr.append(val)
        logger.debug("Added value at index %s, heap size: %s", curr_index, len(self.arr))
        parent_index = curr_index // 2 - (1 - curr_index % 2)
        while res < 0 and parent_index >= 0:
            res = self.comparer.compare(
                self[parent_index], self[curr_index])
            if res < 0:
                logger.debug("Swapping values at indices %s and %s", parent_index, curr_index)
                self.arr[parent_index], self.arr[curr_index] = self[curr_index], self[parent_index]
                curr_index = parent_index
                parent_index = curr_index // 2 - (1 - curr_index % 2)

    def __len__(self):
        return len(self.arr)

    def __getitem__(self, index: int) -> T:
        return self.arr[index]

    def is_empty(self) -> bool:
        """return whether the heap is empty

        Returns:
            bool: result
        """
        return len(self) == 0

    def pop(self) -> T:
        """return the value at the top of the heap while removing it

        Returns:
            Any: the result
        """
        if self.is_empty():
            logger.warning("Attempted to pop from empty heap")
            raise IndexError("pop from empty heap")
        
        logger.debug("Popping from heap, current size: %s", len(self))
        res = self[0]
        self.arr[0], self.arr[-1] = self[-1], self[0]
        self.arr.pop()
        logger.debug("Swapped root with last element, new size: %s", len(self))
        flag = True
        curr_index = 0
        while flag:
            child1_index = curr_index * 2 + 1
            child2_index = curr_index * 2 + 2
            if len(self) > child2_index:
                if self.comparer.compare(self[child1_index], self[child2_index]) < 0:
                    logger.debug("Swapping with right child at index %s", child2_index)
                    self.arr[curr_index], self.arr[child2_index] = self[child2_index], self[curr_index]
                    curr_index = child2_index
                elif self.comparer.compare(self[child1_index], self[child2_index]) > 0:
                    logger.debug("Swapping with left child at index %s", child1_index)
                    self.arr[curr_index], self.arr[child1_index] = self[child1_index], self[curr_index]
                    curr_index = child1_index
                else:
                    logger.debug("Children are equal, heap property satisfied")
                    flag = False
            else:
                if len(self) > child1_index:
                    if self.comparer.compare(self[child1_index], self[curr_index]) > 0:
                        logger.debug("Swapping with only child at index %s", child1_index)
                        self.arr[curr_index], self.arr[child1_index] = self[child1_index], self[curr_index]
                        curr_index = child1_index
                    else:
                        logger.debug("Heap property satisfied with only child")
                        flag = False
                else:
                    logger.debug("No children, heap property satisfied")
                    flag = False
        logger.debug("Heap pop completed, returning: %s", res)
        return res

    def __str__(self):
        return str(self.arr)

    def peek(self) -> T:
        """return the value at the top of the Heap without removing it

        Returns:
            Any: the result
        """
        if self.is_empty():
            logger.warning("Attempted to peek at empty heap")
            raise IndexError("peek at empty heap")
        logger.debug("Peeking at heap top: %s", self[0])
        return self[0]


__all__ = [
    "Heap",
]
