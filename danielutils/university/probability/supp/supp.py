from abc import ABC, abstractmethod
from typing import Iterable


class Supp(ABC, Iterable):
    @abstractmethod
    def intersect(self, other: "Supp") -> "Supp":
        pass


__all__ = [
    "Supp"
]
