from typing import TypeVar, Iterable
from ..custom_types import Consumer

T = TypeVar('T')


def foreach(iterable: Iterable[T], consumer: Consumer[T]) -> None:
    for v in iterable:
        consumer(v)


__all__ = [
    'foreach'
]
