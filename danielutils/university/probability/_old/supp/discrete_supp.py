from typing import Union, Callable
from .supp import Supp
from classes import frange
from .handler_implementations import *
from abc import abstractmethod


class DiscreteSupp(Supp):
    @property
    @abstractmethod
    def inner(self):
        pass

    def __iter__(self):
        yield from self.inner

    def __contains__(self, item):
        return item in self.inner

    @staticmethod
    def _get_handler(lhs: "DiscreteSupp", rhs: "DiscreteSupp") -> Callable[
        ["DiscreteSupp", "DiscreteSupp"], "DiscreteSupp"]:
        k = tuple["DiscreteSupp", "DiscreteSupp"]
        v = Callable[["DiscreteSupp", "DiscreteSupp"], "DiscreteSupp"]
        dct: dict[k, v] = {
            (DiscreteSetSupp, DiscreteSetSupp): discrete_set_discrete_set,
            (DiscreteSetSupp, DiscreteRangeSupp): discrete_set_discrete_range,
            (DiscreteRangeSupp, DiscreteSetSupp): lambda b, a: discrete_set_discrete_range(a, b),
            (DiscreteRangeSupp, DiscreteRangeSupp): discrete_range_discrete_range,
        }
        return dct[(lhs.__class__, rhs.__class__)]

    def intersect(self, other: "DiscreteSupp") -> "DiscreteSupp":
        return DiscreteSupp._get_handler(self, other)(self, other)


class DiscreteSetSupp(DiscreteSupp):
    @property
    def inner(self):
        return self._obj

    def __init__(self, obj: set, is_finite: bool) -> None:
        super().__init__(is_finite)
        self._obj = obj


class DiscreteRangeSupp(DiscreteSupp):
    @staticmethod
    def from_explicit(start: float, stop: float, step: float) -> "DiscreteRangeSupp":
        return DiscreteRangeSupp(frange(start, stop, step))

    @property
    def inner(self):
        return self._obj

    def __init__(self, obj: frange):
        super().__init__(obj.is_finite)
        self._obj = obj


__all__ = [
    "DiscreteSupp",
    "DiscreteSetSupp",
    "DiscreteRangeSupp"
]
