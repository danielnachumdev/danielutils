from .Typing import Any, Type, Sequence, Union, Iterable, Callable


def isoftype(v: Any, t: Any):
    if isinstance(v, (list, tuple)):
        if hasattr(t, '__args__'):
            for subv in v:
                if not isoftype(subv, t.__args__[0]):
                    return False
            return True
        else:
            if t in (list, tuple, Iterable):
                return True
            return False
    elif isinstance(v, dict):
        if hasattr(t, '__args__'):
            keyt, valuet = t.__args__[0], t.__args__[1]
            for key, value in v.items():
                if not isoftype(key, keyt) or not isoftype(value, valuet):
                    return False
            return True
        else:
            if t is dict:
                return True
            return False
    else:  # for instances but also for Union
        if t.__module__ == "typing":
            if t == Any:
                return True
            elif hasattr(v, '__origin__'):
                if v.__origin__ == Union:
                    return type(Union) == t
        elif "Callable" in str(t):
            if v is not Callable and "Callable" in str(v):
                # the case is Callable[[somethings],something]
                if t is type(Callable):
                    return True
                # vargs = v.__args__
                # targs = t.__args__
                pass
        elif hasattr(t, '__origin__'):
            if t.__origin__ == list:
                return False
        elif type(t) == list or type(t) == tuple:
            return isoneof(v, t)
        return isinstance(v, t)


def isoneof(v: Any, types: Union[list[Type], tuple[Type]]) -> bool:
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
    "check_foreach",
    "isoftype"
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
