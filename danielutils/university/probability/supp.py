from typing import Iterator, TypeVar

T = TypeVar('T')


class Supp(Iterator[T]): ...


class DiscreteSupp(Supp[int]):
    def __next__(self):
        yield from self

    def __init__(self, r: range):
        self._r = r

    def __iter__(self) -> Iterator[int]:
        return iter(self._r)


class ContinuseSupp(Supp[float]): ...


__all__ = [
    "Supp",
    "DiscreteSupp",
    "ContinuseSupp",
]
