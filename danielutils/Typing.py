
from typing import Any, Iterable, Optional, NoReturn, TypeAlias, Union, Concatenate, Literal, ClassVar, Final, Annotated, TypeGuard, Generic, TypeVar, ParamSpec, NewType, IO, get_args, get_origin, get_type_hints
from collections.abc import Callable, Sequence
from builtins import tuple, list, dict, type
List = list


class Tuple(tuple):
    pass


Dict = dict
Type = type


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


__all__ = [
    "isoftype",
    "Any",
    "Iterable",
    "Optional",
    "NoReturn",
    "TypeAlias",
    "Union",
    "Literal",
    "ClassVar",
    "Final",
    "Annotated",
    "TypeGuard",
    "Generic",
    "TypeVar",
    "ParamSpec",
    "NewType",
    "danielutils.IO",
    "Callable",
    "Sequence",
    "tuple",
    "list",
    "dict",
    "type",
    "tuple"
]
