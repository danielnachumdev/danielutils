from typing import Iterable, Optional, Generator, Any
import itertools


def powerset(iterable: Iterable[Any], length: Optional[int] = None) -> Generator[tuple, None, None]:
    """returns the powerset of specified length of an iterable
    """
    if length is None:
        if hasattr(iterable, "__len__"):
            length = len(iterable)  # type:ignore
        else:
            raise ValueError(
                "when using powerset must supply length explicitly or object should support len()")
    for i in range(length+1):
        yield from itertools.combinations(iterable, i)


__all__ = [
    "powerset"
]
