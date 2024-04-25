from typing import Protocol, TypeVar, runtime_checkable,Dict as t_dict
from ..reflection import get_python_version

if get_python_version() >= (3, 9):
    from builtins import dict as t_dict

K = TypeVar('K')
V = TypeVar('V')

@runtime_checkable
class Dictable(Protocol[K, V]):
    @classmethod
    def from_dict(cls, d: t_dict[K, V]) -> 'Dictable[K,V]': ...

    def to_dict(self) -> t_dict[K, V]: ...


__all__ = [
    'Dictable'
]
