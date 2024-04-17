from typing import runtime_checkable, Protocol, TypeVar

T = TypeVar('T')


@runtime_checkable
class Evaluable(Protocol[T]):
    def evaluate(self, *args, **kwargs) -> T: ...


__all__ = ['Evaluable']
