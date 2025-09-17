import logging
from typing import Any, Union, Sequence
from .isoftype import isoftype
from ..reflection import get_python_version
from .logging_.utils import get_logger

logger = get_logger(__name__)
if get_python_version() < (3, 9):
    from typing import List as List, Tuple as Tuple
else:
    from builtins import list as List, tuple as Tuple  # type:ignore


def isoneof(v: Any, types: Union[List[type], Tuple[type]]) -> bool:
    """performs isoftype() or ... or isoftype()

    Args:
        v (Any): the value to check it's type
        types (Union[list[Type], tuple[Type]): A Sequence of approved types

    Raises:
        TypeError: if the second argument is not from Union[list[Type], tuple[Type]

    Returns:
        bool: return True iff isoftype(v, types[0]) or ... isoftype(v, types[...])
    """
    logger.debug(f"Checking if {v} is one of types: {types}")
    if not isinstance(types, (list, tuple)):
        logger.error("'types' parameter must be of type 'list' or 'tuple'")
        raise TypeError("'types' must be of type 'list' or 'tuple'")
    
    for i, T in enumerate(types):
        if isoftype(v, T):
            logger.debug(f"Value {v} matches type at index {i}: {T}")
            return True
    
    logger.debug(f"Value {v} does not match any of the specified types")
    return False


def isoneof_strict(v: Any, types: Union[List[type], Tuple[type]]) -> bool:
    """performs 'type(v) in types' efficiently

    Args:
        v (Any): value to check
        types (Sequence[Type]): sequence of approved types

    Raises:
        TypeError: if types is not a sequence

    Returns:
        bool: true if type of value appears in types
    """
    logger.debug(f"Strict type checking if {v} (type: {type(v)}) is one of: {types}")
    if not isinstance(types, Sequence):
        logger.error("'types' parameter must be of type Sequence")
        raise TypeError("lst must be of type Sequence")
    
    for i, T in enumerate(types):
        if type(v) in {T}:
            logger.debug(f"Value {v} type matches at index {i}: {T}")
            return True
    
    logger.debug(f"Value {v} type does not match any of the specified types")
    return False


__all__ = [
    "isoneof",
    "isoneof_strict"
]
