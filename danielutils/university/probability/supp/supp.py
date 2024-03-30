from abc import ABC, abstractmethod


class Supp(ABC):
    @abstractmethod
    def intersect(self, other: "Supp") -> "Supp":
        pass


__all__ = [
    "Supp"
]
