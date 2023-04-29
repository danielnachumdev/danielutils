from typing import Callable, Any
from .Heap import Heap
from .Comparer import Comparer
from .functions import default_weight_function


class Queue:
    """classic Queue data structure"""

    def __init__(self):
        self.data = []

    def pop(self) -> Any:
        """return the oldest element while removing it from the queue

        Returns:
            Any: result
        """
        return self.data.pop()

    def push(self, value: Any) -> None:
        """adds a new element to the queue

        Args:
            value (Any): the value to add
        """
        self.data.append(value)

    def peek(self) -> Any:
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
        return str(self.data)

    def __iter__(self):
        while not self.is_empty():
            yield self.pop()

    def push_many(self, arr: list):
        """will push many objects to the Queue

        Args:
            arr (list): the objects to push
        """
        for v in arr:
            self.push(v)


class PriorityQueue(Queue):
    """
    A priority queue implementation based on a binary heap.

    Args:
        weight_func (Callable[[T], int | float], optional): A function to calculate the weight of items added
            to the queue. Defaults to default_weight_function.
        comparer (Comparer, optional): The comparer to use when comparing weights of items in the queue.
            Defaults to Comparer.GREATER.

    Raises:
        ValueError: Raised if an item with the same weight value is added more than once.

    Methods:
        pop() -> T:
            Removes and returns the item with the highest priority (i.e., the lowest weight value) from the queue.
        push(value: T):
            Adds a new item to the queue with the specified value and weight.
        peek() -> T:
            Returns the item with the highest priority 
            (i.e., the lowest weight value) from the queue without removing it.
        __str__() -> str:
            Returns a string representation of the queue.

    Example:
        >>> pq = PriorityQueue()
        >>> pq.push(5)
        >>> pq.push(3)
        >>> pq.push(10)
        >>> pq.pop()
        3
    """

    def __init__(self, weight_func: Callable[[Any], int | float] = default_weight_function,
                 comparer: Comparer = Comparer.GREATER):
        super().__init__()
        self.data = Heap(comparer)
        self.weight_func = weight_func
        self.dct = {}

    def pop(self) -> Any:
        """
        Removes and returns the item with the highest priority (i.e., the lowest weight value) from the queue.

        Returns:
            T: The item with the highest priority in the queue.

        Raises:
            KeyError: Raised if the queue is empty.
        """
        item_weight = self.data.pop()
        res = self.dct[item_weight]
        del self.dct[item_weight]
        return res

    def push(self, value: Any):
        """
        Adds a new item to the queue with the specified value and weight.

        Args:
            value (T): The value of the item to add to the queue.

        Returns:
            None

        Raises:
            ValueError: Raised if an item with the same weight value is added more than once.
        """
        item_weight = self.weight_func(value)
        if item_weight in self.dct:
            raise ValueError(
                "Can't have same weight value more than once in current implementation")
        self.data.push(item_weight)
        self.dct[item_weight] = value

    def peek(self) -> Any:
        """
        Returns the item with the highest priority (i.e., the lowest weight value) from the queue without removing it.

        Returns:
            T: The item with the highest priority in the queue.

        Raises:
            KeyError: Raised if the queue is empty.
        """
        return self.dct[self.data.peek()]

    def __str__(self) -> str:
        """
        Returns a string representation of the queue.

        Returns:
            str: A string representation of the queue.
        """
        return str([str(self.dct[w]) for w in [self.data[i] for i in range(len(self.data))]])


__all__ = [
    "Queue",
    "PriorityQueue"
]
