from abc import abstractmethod, ABC
from typing import Iterator, TypeVar, Union
from ...better_builtins import frange
from ...decorators import memo

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
    def minimum(self) -> float: ...

    @property
    @abstractmethod
    def maximum(self) -> float: ...


class DiscreteSupp(Supp[int]):
    pass


class FrangeSupp(DiscreteSupp):
    @property
    def is_finite(self) -> bool:
        if isinstance(self._r, frange):  # type:ignore
            return self._r.is_finite  # type:ignore
        return True

    def __next__(self):
        yield from self

    def __init__(self, r: Union[range, frange]): # type:ignore
        self._r: frange = r if isinstance(r, frange) else frange.from_range(r)  # type:ignore

    def __iter__(self) -> Iterator[int]:
        return iter(self._r)

    def __contains__(self, item) -> bool:
        return item in self._r  # type:ignore

    @property
    def minimum(self) -> float:
        return self._r.start  # type:ignore

    @property
    def maximum(self) -> float:
        return self._r.stop  # type:ignore

    @property
    def step(self) -> float:
        return self._r.step  # type:ignore


class SetSupp(DiscreteSupp):
    @property
    def is_finite(self) -> bool:
        return True

    @property
    @memo  # type:ignore
    def minimum(self) -> float:
        return min(self._s)

    @property
    @memo  # type:ignore
    def maximum(self) -> float:
        return max(self._s)

    def __init__(self, s: set) -> None:
        self._s = s

    def __iter__(self) -> Iterator:
        return iter(self._s)

    def __contains__(self, item) -> bool:
        return item in self._s


class ContinuseSupp(Supp[float]):

    @property
    def is_finite(self) -> bool:
        return False


__all__ = [
    "Supp",
    "FrangeSupp",
    "ContinuseSupp",
]
