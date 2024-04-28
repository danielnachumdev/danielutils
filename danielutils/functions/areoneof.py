from typing import Sequence, Any, Union
from .isoneof import isoneof
from ..reflection import get_python_version
if get_python_version() < (3, 9):
    from typing import List as List, Tuple as Tuple
else:
    from builtins import list as List, tuple as Tuple  # type:ignore


def areoneof(values: Sequence[Any], types: Union[List[type], Tuple[type]]) -> bool:
    """performs 'isoneof(values[0],types) and ... and isoneof(values[...],types)'

    Args:
        values (Sequence[Any]): Sequence of values
        types (Sequence[Type]): Sequence of types

    Raises:
        TypeError: if types is not a Sequence
        TypeError: if values is not a Sequence

    Returns:
        bool: the result of the check
    """
    if not isinstance(types, Sequence):
        raise TypeError("'types' must be of type Sequence")
    if not isinstance(values, Sequence):
        raise TypeError("'values' must be of type Sequence")
    for v in values:
        if not isoneof(v, types):
            return False
    return True


__all__ = [
    "areoneof"
]
