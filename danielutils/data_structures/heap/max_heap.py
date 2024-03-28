from typing import TypeVar
from ..comparer import CompareGreater
from .heap import Heap

T = TypeVar("T")


class MaxHeap(Heap[T]):
    """classic MaxHeap implementation
    """

    def __init__(self):
        super().__init__(CompareGreater)


__all__ = [
    "MaxHeap"
]
