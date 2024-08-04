from typing import TypeVar, Generic

from ..java_interface import JavaInterface

T = TypeVar('T')


class Comparable(JavaInterface, Generic[T]):
    def __lt__(self, other: T) -> bool: ...

    def __gt__(self, other: T) -> bool: ...

    def __eq__(self, other: T) -> bool: ...

    def __le__(self, other: T) -> bool: ...

    def __ge__(self, other: T) -> bool: ...

    def __ne__(self, other: T) -> bool: ...


__all__ = [
    "Comparable",
]
