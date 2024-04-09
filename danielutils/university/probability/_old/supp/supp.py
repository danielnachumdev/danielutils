from abc import ABC, abstractmethod
from typing import Iterable


class Supp(ABC, Iterable):
    @property
    def is_finite(self) -> bool:
        return self._is_finite

    @property
    def is_infinite(self) -> bool:
        return not self.is_finite

    def __init__(self, is_finite: bool) -> None:
        self._is_finite = is_finite

    @abstractmethod
    def intersect(self, other: "Supp") -> "Supp":
        pass


__all__ = [
    "Supp"
]
