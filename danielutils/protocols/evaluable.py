from abc import abstractmethod
from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar('T', covariant=True)


@runtime_checkable
class Evaluable(Protocol[T]):
    @abstractmethod
    def evaluate(self) -> T: ...


__all__ = [
    "Evaluable"
]
