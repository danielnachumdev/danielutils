from abc import ABC, abstractmethod
from typing import Any


class Encoding(ABC):
    @abstractmethod
    def encode(self, obj: Any) -> bytes: ...

    @abstractmethod
    def decode(self, obj: bytes) -> Any: ...


__all__ = [
    'Encoding'
]
