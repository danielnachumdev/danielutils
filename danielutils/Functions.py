from typing import Any, Type, Callable, Sequence


def isoneof(v: Any, types: Sequence[Type]) -> bool:
    """performs isinstance() or ... or isinstance()

    Args:
        v (Any): the value to check it's type
        types (Sequence[Type]): A Sequence of approved types

    Raises:
        TypeError: if the second argument is not a Sequence

    Returns:
        bool: return True iff isinstance(v, types[0]) or ... isinstance(v, types[...])
    """
    if not isinstance(types, Sequence):
        raise TypeError("'types' must be of type Sequence")
    for T in types:
        if isinstance(v, T):
            return True
    return False


def isoneof_strict(v: Any, types: Sequence[Type]) -> bool:
    """performs 'type(v) in types' efficently

    Args:
        v (Any): value to check
        types (Sequence[Type]): ssequence of aprroved types

    Raises:
        TypeError: if types is not a sequence

    Returns:
        bool: true if type of value appers in types
    """
    if not isinstance(types, Sequence):
        raise TypeError("lst must be of type Sequence")
    for T in types:
        if type(v) == T:
            return True
    return False


def areoneof(values: Sequence[Any], types: Sequence[Type]) -> bool:
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


def check_foreach(values: Sequence[Any], condition: Callable[[Any], bool]) -> bool:
    """

    Args:
        values (Sequence[Any]): Values to perform check on
        condition (Callable[[Any], bool]): Condition to check on all values

    Returns:
        bool: returns True iff condition return True for all values individually
    """
    if not isinstance(values, Sequence):
        pass
    if not isinstance(condition, Callable):
        pass
    for v in values:
        if not condition(v):
            return False
    return True


__all__ = [
    "isoneof",
    "isoneof_strict",
    "areoneof",
    "check_foreach"
]
# def almost_equal(*args: Sequence[Any], func: Callable[[Any, Any, Any], bool] = math.isclose, diff: Any = 0.00000000001) -> bool:
#     """checks wheter all values are within absolute range of each other in O(n**2)

#     Args:
#         func (Callable[[Any, Any, Any], bool], optional): function to check. Defaults to math.isclose.
#         diff (Any, optional): default absolute tolerance. Defaults to 0.00000000001.

#     Returns:
#         bool: return True if all values are within specified tolerande from all other values
#     """
#     for i in range(len(args)):
#         for j in range(i+1, len(args)):
#             if func is math.isclose:
#                 if not func(args[i], args[j], abs_tol=diff):
#                     return False
#             else:
#                 if not func(args[i], args[j], diff):
#                     return False
#     return True
