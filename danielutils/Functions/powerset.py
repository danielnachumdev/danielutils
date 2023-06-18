from typing import Iterable, Optional, Generator
import itertools


def powerset(iterable: Iterable, length: Optional[int] = None) -> Generator[tuple, None, None]:
    if length is None:
        length = len(iterable)
    for i in range(length+1):
        yield from itertools.combinations(iterable, i)


__all__ = [
    "powerset"
]
