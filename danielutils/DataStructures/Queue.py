from .Heap import Heap
from .Comparer import Comparer
from .functions import weight
from typing import Callable, Any, TypeVar
T = TypeVar("T")


class Queue:
    def __init__(self):
        self.data = []

    def pop(self):
        return self.data.pop()

    def push(self, value):
        self.data.append(value)

    def peek(self):
        return self.data[-1]


class PriorityQueue:
    def __init__(self, weight_func: Callable[[T], int | float] = weight, comparer: Comparer = Comparer.GREATER):
        self.heap = Heap(comparer)
        self.weight = weight_func
        self.dct = dict()

    def pop(self) -> T:
        w = self.heap.pop()
        res = self.dct[w]
        del self.dct[w]
        return res

    def push(self, value: T):
        w = self.weight(value)
        if w in self.dct:
            raise ValueError(
                "Can't have same weight value more than once in current implementation")
        self.heap.push(w)
        self.dct[w] = value

    def peek(self) -> T:
        return self.dct[self.heap.peek()]

    def __str__(self) -> str:
        return str([str(self.dct[w]) for w in [self.heap[i] for i in range(len(self.heap))]])


__all__ = [
    "PriorityQueue"
]
