from typing import TypeVar
from ..comparer import CompareSmaller
from .heap import Heap

T = TypeVar("T")


class MinHeap(Heap[T]):
    """classic MinHeap implementation
    """

    def __init__(self) -> None:
        super().__init__(CompareSmaller)


__all__ = [
    "MinHeap"
]
