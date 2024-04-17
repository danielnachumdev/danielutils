from typing import Iterator, TypeVar, Union
from ...classes import frange

T = TypeVar('T')


class Supp(Iterator[T]): ...


class DiscreteSupp(Supp[int]):
    def __next__(self):
        yield from self

    def __init__(self, r: Union[range, frange]):
        self._r = r

    def __iter__(self) -> Iterator[int]:
        return iter(self._r)


class ContinuseSupp(Supp[float]): ...


__all__ = [
    "Supp",
    "DiscreteSupp",
    "ContinuseSupp",
]
