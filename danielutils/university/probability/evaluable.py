from abc import ABC, abstractmethod
from typing import Any


class Evaluable(ABC):
    @abstractmethod
    def evaluate(self, *args, **kwargs) -> Any: ...


__all__ = [
    "Evaluable"
]
