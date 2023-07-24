from typing import Sequence, Any, Union
from .isoneof import isoneof
from ..Reflection import get_python_version
if get_python_version() < (3, 9):
    from typing import List as t_list, Tuple as t_tuple
else:
    from builtins import list as t_list, tuple as t_tuple  # type:ignore


def areoneof(values: Sequence[Any], types: Union[t_list[type], t_tuple[type]]) -> bool:
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
