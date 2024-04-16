from typing import Protocol, TypeVar, runtime_checkable

T = TypeVar('T')


@runtime_checkable
class Evaluable(Protocol[T]):
    def evaluate(self) -> T: ...


__all__ = [
    "Evaluable"
]
