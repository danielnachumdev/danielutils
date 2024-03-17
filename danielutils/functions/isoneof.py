from typing import Any, Union, Sequence
from .isoftype import isoftype
from ..reflection import get_python_version
if get_python_version() < (3, 9):
    from typing import List as t_list, Tuple as t_tuple
else:
    from builtins import list as t_list, tuple as t_tuple  # type:ignore


def isoneof(v: Any, types: Union[t_list[type], t_tuple[type]]) -> bool:
    """performs isoftype() or ... or isoftype()

    Args:
        v (Any): the value to check it's type
        types (Union[list[Type], tuple[Type]): A Sequence of approved types

    Raises:
        TypeError: if the second argument is not from Union[list[Type], tuple[Type]

    Returns:
        bool: return True iff isoftype(v, types[0]) or ... isoftype(v, types[...])
    """
    if not isinstance(types, (list, tuple)):
        raise TypeError("'types' must be of type 'list' or 'tuple'")
    for T in types:
        if isoftype(v, T):
            return True
    return False


def isoneof_strict(v: Any, types: Union[t_list[type], t_tuple[type]]) -> bool:
    """performs 'type(v) in types' efficiently

    Args:
        v (Any): value to check
        types (Sequence[Type]): sequence of approved types

    Raises:
        TypeError: if types is not a sequence

    Returns:
        bool: true if type of value appears in types
    """
    if not isinstance(types, Sequence):
        raise TypeError("lst must be of type Sequence")
    for T in types:
        if type(v) in {T}:
            return True
    return False


__all__ = [
    "isoneof",
    "isoneof_strict"
]
