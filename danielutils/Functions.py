from .Typing import Any, type, Sequence, Union, Iterable, Callable
from typing import get_args, get_origin, get_type_hints


def __isoftype_inquire(obj: Any) -> tuple[Any, Any, Any]:
    origin = None
    args = None
    type_hints = None
    try:
        origin = get_origin(obj)
    except:
        pass
    try:
        args = get_args(obj)
    except:
        pass
    try:
        type_hints = get_type_hints(obj)
    except:
        pass
    return origin, args, type_hints


def isoftype(obj: Any, T: Any) -> bool:
    obj_origin, obj_args, obj_hints = __isoftype_inquire(obj)
    t_origin, t_args, t_hints = __isoftype_inquire(T)
    if t_origin is not None:
        if t_origin in {list}:
            for sub_v in obj:
                if not isoftype(sub_v, t_args[0]):
                    return False
            return True
        elif t_origin is dict:
            key_t, value_t,  = t_args[0], t_args[1]
            for k, v in obj.items():
                if not isoftype(v, value_t):
                    return False
                if not isoftype(k, key_t):
                    return False
            return True
        elif t_origin in {Union}:
            for sub_t in t_args:
                if isoftype(obj, sub_t):
                    return True
            return False
        elif t_origin in {Callable}:
            if obj.__name__ == "<lambda>":
                return True
            tmp = list(obj_hints.values())
            obj_return_type = tmp[-1]
            obj_param_types = tuple(tmp[:-1])
            del tmp
            t_return_type = t_args[1]
            t_param_types = tuple(t_args[0])
            return obj_return_type is t_return_type and obj_param_types == t_param_types
    else:
        if T is Any:
            return True
        elif type(T) in {list}:
            for sub_t in T:
                if isoftype(obj, sub_t):
                    return True
            return False
        elif obj_origin is not None:
            if obj_origin is Union:
                return T is type(Union)
    return isinstance(obj, T)


# def isoftype(v: Any, t: Any):
#     if isinstance(v, (list, tuple)):
#         if hasattr(t, '__args__'):
#             for sub_v in v:
#                 if not isoftype(sub_v, t.__args__[0]):
#                     return False
#             return True
#         else:
#             if t in (list, tuple, Iterable):
#                 return True
#             return False
#     elif isinstance(v, dict):
#         if hasattr(t, '__args__'):
#             key_t, value_t = t.__args__[0], t.__args__[1]
#             for key, value in v.items():
#                 if not isoftype(key, key_t) or not isoftype(value, value_t):
#                     return False
#             return True
#         else:
#             if t is dict:
#                 return True
#             return False
#     else:  # for instances but also for Union
#         if t.__module__ == "typing":
#             if t == Any:
#                 return True
#             elif hasattr(v, '__origin__'):
#                 if v.__origin__ == Union:
#                     return type(Union) == t
#         elif "Callable" in str(t):
#             if v is not Callable and "Callable" in str(v):
#                 # the case is Callable[[somethings],something]
#                 if t is type(Callable):
#                     return True
#                 # v_args = v.__args__
#                 # t_args = t.__args__
#                 pass
#         elif hasattr(t, '__origin__'):
#             if isinstance(t.__origin__, list):
#                 return False
#         elif type(t) == list or type(t) == tuple:
#             return isoneof(v, t)
#         return isinstance(v, t)


def isoneof(v: Any, types: Union[list[type], tuple[type]]) -> bool:
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


def isoneof_strict(v: Any, types: Sequence[type]) -> bool:
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
        if type(v) == T:
            return True
    return False


def areoneof(values: Sequence[Any], types: Sequence[type]) -> bool:
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


def get_source_code(obj: object) -> list[str]:
    if not isinstance(obj, object):
        raise ValueError("obj must be an object")
    import inspect
    return inspect.getsource(obj)


__all__ = [
    "isoneof",
    "isoneof_strict",
    "areoneof",
    "check_foreach",
    "isoftype",
    "get_source_code"
]
# def almost_equal(*args: Sequence[Any], func: Callable[[Any, Any, Any], bool] = math.isclose, diff: Any = 0.00000000001) -> bool:
#     """checks whether all values are within absolute range of each other in O(n**2)

#     Args:
#         func (Callable[[Any, Any, Any], bool], optional): function to check. Defaults to math.isclose.
#         diff (Any, optional): default absolute tolerance. Defaults to 0.00000000001.

#     Returns:
#         bool: return True if all values are within specified tolerance from all other values
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
