import logging
from typing import Protocol, TypeVar, runtime_checkable,Dict as Dict
from ..reflection import get_python_version
from ..logging_.utils import get_logger

logger = get_logger(__name__)

if get_python_version() >= (3, 9):
    from builtins import dict as Dict

K = TypeVar('K')
V = TypeVar('V')

@runtime_checkable
class Dictable(Protocol[K, V]):
    @classmethod
    def from_dict(cls, d: Dict[K, V]) -> 'Dictable[K,V]':
        """
        Create a Dictable object from a dictionary.
        
        Note: This is a protocol method. Implementations should add logging
        to track dictionary conversion operations.
        """
        ...

    def to_dict(self) -> Dict[K, V]:
        """
        Convert the object to a dictionary.
        
        Note: This is a protocol method. Implementations should add logging
        to track dictionary conversion operations.
        """
        ...


__all__ = [
    'Dictable'
]
