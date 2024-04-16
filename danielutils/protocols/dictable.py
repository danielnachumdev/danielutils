from typing import Protocol, TypeVar, runtime_checkable

K = TypeVar('K')
V = TypeVar('V')

@runtime_checkable
class Dictable(Protocol[K, V]):
    @classmethod
    def from_dict(cls, d: dict[K, V]) -> 'Dictable[K,V]': ...

    def to_dict(self) -> dict[K, V]: ...


__all__ = [
    'Dictable'
]
