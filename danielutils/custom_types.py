from typing import Callable, TypeVar, Generic

try:
    from typing import TypeAlias
except ImportError:
    from typing_extensions import TypeAlias

T = TypeVar('T')
U = TypeVar('U')
Procedure: TypeAlias = Callable[[], None]
Supplier: TypeAlias = Callable[[], T]
Consumer: TypeAlias = Callable[[T], None]
Predicate: TypeAlias = Callable[[], bool]
Mapper: TypeAlias = Callable[[T], U]

__all__ = [
    'Procedure',
    'Supplier',
    'Consumer',
    'Predicate',
    'Mapper'
]
