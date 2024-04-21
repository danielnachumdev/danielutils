from abc import abstractmethod, ABC
from typing import Iterator, TypeVar, Union
from ...better_builtins import frange

T = TypeVar('T')


class Supp(ABC, Iterator[T]):
    @property
    @abstractmethod
    def is_finite(self) -> bool: ...

    def is_infinite(self) -> bool:
        return not self.is_finite

    @abstractmethod
    def __contains__(self, item) -> bool: ...

    @property
    @abstractmethod
    def start(self) -> float: ...

    @property
    @abstractmethod
    def stop(self) -> float: ...


class DiscreteSupp(Supp[int]):
    @property
    def is_finite(self) -> bool:
        if isinstance(self._r, frange):
            return self._r.is_finite
        return True

    def __next__(self):
        yield from self

    def __init__(self, r: Union[range, frange]):
        self._r = r

    def __iter__(self) -> Iterator[int]:
        return iter(self._r)

    def __contains__(self, item) -> bool:
        return item in self._r

    @property
    def start(self) -> float:
        return self._r.start

    @property
    def stop(self) -> float:
        return self._r.stop

    @property
    def step(self) -> float:
        return self._r.step


class ContinuseSupp(Supp[float]):

    @property
    def is_finite(self) -> bool:
        return False


__all__ = [
    "Supp",
    "DiscreteSupp",
    "ContinuseSupp",
]
