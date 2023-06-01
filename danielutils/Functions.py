from typing import get_args, get_origin, get_type_hints, Any, Sequence, Union, TypeVar, ForwardRef, Literal, Optional, cast
from collections.abc import Callable, Generator, Iterable
import inspect


def get_function_return_type(func: Callable, signature: Optional[inspect.Signature] = None) -> Optional[type]:
    """returns the return type of a function

    Args:
        func (Callable): a function to inquire about

    Returns:
        Optional[type]: the return type of the function
    """
    if signature is None:
        signature = inspect.signature(func)
    if ("inspect._empty" in str(signature.return_annotation)) or (signature.return_annotation is None):
        return type(None)
    return signature.return_annotation


def __isoftype_inquire(obj: Any) -> tuple[Optional[type], Optional[tuple], Optional[dict]]:
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


implicit_union_type = type(int | str)
ellipsis_ = ...


def isoftype(obj: Any, T: Any, /, strict: bool = True) -> bool:
    """Checks if an object is of the given type or any of its subtypes.

    Args:
        obj (Any): The object to be checked.
        T (Any): The type or types to be checked against.

    Returns:
        bool: True if the object is of the given type or any of its subtypes, False otherwise.
    """
    if not isinstance(strict, bool):
        raise TypeError("'strict' must be of type bool")
    obj_origin, obj_args, obj_hints = __isoftype_inquire(obj)
    t_origin, t_args, t_hints = __isoftype_inquire(T)
    if t_args is not None and ellipsis_ in t_args:
        from .Colors import warning
        warning(
            "using an ellipsis (as in '...') with isoftype is ambiguous returning False")
        return False
    if t_origin is not None:
        t_args = cast(tuple, t_args)
        if t_origin in {list, tuple, dict, dict, Iterable}:
            if not isinstance(obj, t_origin):
                return False

            if t_origin in {list, set, Iterable}:
                obj = cast(Iterable, obj)
                value_t = t_args[0]
                for value in obj:
                    if not isoftype(value, value_t, strict=strict):
                        return False
                return True

            elif t_origin is tuple:
                obj = cast(tuple, obj)
                if len(obj) != len(t_args):
                    return False
                for sub_obj, sub_t in zip(obj, t_args):
                    if not isoftype(sub_obj, sub_t, strict=strict):
                        return False
                return True

            elif t_origin is dict:
                obj = cast(dict, obj)
                key_t, value_t,  = t_args[0], t_args[1]
                for k, v in obj.items():
                    if not isoftype(k, key_t, strict=strict):
                        return False
                    if not isoftype(v, value_t, strict=strict):
                        return False
                return True

        elif t_origin in {Union, implicit_union_type}:  # also handle typing.Optional
            for sub_t in t_args:
                if isoftype(obj, sub_t, strict=strict):
                    return True
            return False

        elif t_origin is Generator:
            yield_t, send_t, return_t = t_args
            return isinstance(obj, Generator)

        elif t_origin is Literal:
            for literal in t_args:
                if obj is literal:
                    return True
            return False

        elif t_origin is Callable:
            obj_hints = cast(dict, obj_hints)

            if not callable(obj):
                return False
            if obj.__name__ == "<lambda>":
                if strict:
                    from .Colors import warning
                    warning("using lambda function with isoftype is ambiguous")
                return not strict
            if len(t_args) == 0:
                return True
            tmp = list(obj_hints.values())
            obj_return_type = tmp[-1] if tmp else None
            obj_param_types = tuple(tmp[:-1]) if tmp else None
            del tmp
            t_return_type = t_args[1]
            t_param_types = tuple(t_args[0])
            return obj_return_type is t_return_type and obj_param_types == t_param_types

        else:
            from .Colors import warning
            from .Reflection import get_traceback
            warning(
                f"In function isoftype, unhandled t_origin: {t_origin} returning True. stacktrace:")
            print(*get_traceback())
            return True
    else:
        if T is Any:
            return True

        elif type(T) in {list, tuple}:
            # if T == (int,) or something
            for sub_t in T:
                if isoftype(obj, sub_t, strict=strict):
                    return True
            return False

        elif obj_origin is not None:
            if obj_origin is Union:
                return T is type(Union)

        elif isinstance(T, TypeVar):
            t_args = T.__constraints__
            if t_args:
                for sub_t in t_args:
                    if isoftype(obj, sub_t):
                        return True
                return False
            # TODO how should we check that all value in the same relative position are of the same type
            return True

        elif isinstance(T, ForwardRef):
            # TODO what happens if there are a few classes with the same name from different modules? this will break
            name_of_type = T.__forward_arg__
            return type(obj).__name__ == name_of_type

    return isinstance(obj, T)


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


def isoneof_strict(v: Any, types: Union[list[type], tuple[type]]) -> bool:
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


def areoneof(values: Sequence[Any], types: Union[list[type], tuple[type]]) -> bool:
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
    if not callable(condition):
        pass
    for v in values:
        if not condition(v):
            return False
    return True


__all__ = [
    "isoftype",
    "get_function_return_type",
    "isoneof",
    "isoneof_strict",
    "areoneof",
    "check_foreach",
]
