from typing import get_args, get_origin, get_type_hints, Any, Union, TypeVar, \
    ForwardRef, Literal, Optional, Tuple as t_tuple, Protocol
from collections.abc import Callable, Generator, Iterable
from ..reflection import get_python_version

if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec, Concatenate
else:

    # pylint: disable=ungrouped-imports
    from typing import ParamSpec, Concatenate  # type:ignore
    from builtins import tuple as t_tuple  # type:ignore
# implicit_union_type = type(int | str)
concatenate_t = type(Concatenate[str, ParamSpec("P_")])
ellipsis_ = ...


def __isoftype_inquire(obj: Any) -> t_tuple[Optional[type], Optional[tuple], Optional[dict]]:
    """
    Inquires the origin, arguments, and type hints of an object.

    Args:
        obj: The object to inquire.

    Returns:
        A tuple containing the origin, arguments, and type hints of the object.
    """
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


def __handle_list_set_iterable(params: tuple) -> bool:
    """
    Handles the 'list', 'set', and 'Iterable' origin types.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the 'list', 'set', or 'Iterable' origin type, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    value_t = t_args[0]
    for value in V:
        if not isoftype(value, value_t, strict=strict):
            return False
    return True


def __handle_tuple(params: tuple) -> bool:
    """
    Handles the 'tuple' origin type.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the 'tuple' origin type, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    if len(V) != len(t_args):
        return False
    for sub_obj, sub_t in zip(V, t_args):
        if not isoftype(sub_obj, sub_t, strict=strict):
            return False
    return True


def __handle_dict(params: tuple) -> bool:
    """
    Handles the 'dict' origin type.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the 'dict' origin type, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    key_t, value_t = t_args[0], t_args[1]
    for k, v in V.items():
        if not isoftype(k, key_t, strict=strict):
            return False
        if not isoftype(v, value_t, strict=strict):
            return False
    return True


def __handle_union(params: tuple) -> bool:
    """
    Handles the 'Union' origin type.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the 'Union' origin type, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    for sub_t in t_args:
        if isoftype(V, sub_t, strict=strict):
            return True
    return False


def __handle_generator(params: tuple) -> bool:
    """
    Handles the 'Generator' origin type.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the 'Generator' origin type, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    yield_t, send_t, return_t = t_args
    return isinstance(V, Generator)


def __handle_literal(params: tuple) -> bool:
    """
    Handles the 'Literal' origin type.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the 'Literal' origin type, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    for literal in t_args:
        if V is literal:
            return True
    return False


def __handle_callable(params: tuple) -> bool:
    """
    Handles the 'Callable' origin type.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the 'Callable' origin type, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params

    if not callable(V):
        return False

    if V.__name__ == "<lambda>":
        if strict:
            print("Using lambda function with isoftype is ambiguous.")
        return not strict

    if t_args is None:
        return True
    if len(t_args) == 0:
        return True

    if get_python_version() < (3, 9):
        if isoftype(t_args[0][0], [ParamSpec, concatenate_t]):
            return True
    else:
        if isoftype(t_args[0], [ParamSpec, concatenate_t]):
            return True

    obj_return_type = obj_hints.get('return')
    obj_param_types = list(obj_hints.values())[:-1] if obj_hints else None
    t_return_type = t_args[1]

    if isinstance(t_args[0], Iterable):
        t_param_types = list(t_args[0])
        A = obj_param_types + [obj_return_type] if obj_param_types else None
        B = t_param_types + [t_return_type]

        if A is None or B is None or len(A) != len(B):
            return False
        for a, b in zip(A, B):
            if hasattr(b, "__args__"):  # Union
                if a not in b.__args__:
                    return False
            elif a is not b:  # otherwise
                return False
        return True

    return False


def __handle_type_origin(params: tuple) -> bool:
    """
    Handles the type origin.

    Args:
        params: A tuple containing the required parameters.

    Returns:
        True if the object matches the type origin, False otherwise.
    """
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    if T is Any:
        return True

    if type(T) in (list, tuple):
        for sub_t in T:
            if isoftype(V, sub_t, strict=strict):
                return True
        return False

    if obj_origin is not None and obj_origin is Union:
        return T is type(Union)

    if isinstance(T, TypeVar):
        t_args = T.__constraints__
        if t_args:
            for sub_t in t_args:
                if isoftype(V, sub_t):
                    return True
            return False

        return True

    if isinstance(T, ForwardRef):
        name_of_type = T.__forward_arg__
        return type(V).__name__ == name_of_type

    return isinstance(V, T)


def __handle_protocol(params: tuple) -> bool:
    from ..reflection import FunctionDeclaration
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    if not isoftype(V, type):
        return False

    if not isinstance(V, t_origin):
        return False

    declared_funcs: list[FunctionDeclaration] = list(FunctionDeclaration.get_declared_functions(V))
    required_funcs: list[FunctionDeclaration] = list(FunctionDeclaration.get_declared_functions(t_origin))

    for i, req_func in enumerate(required_funcs):
        if req_func.has_generics:
            if req_func.return_type in req_func.generics:
                new_req_func = req_func.duplicate(
                    return_type=t_args[req_func.generics.index(req_func.return_type)].__name__)
                required_funcs[i] = new_req_func
            for arg in required_funcs[i].arguments:
                for generic in req_func.generics:
                    if arg.type is not None and generic in arg.type:
                        pass
    return len(set(required_funcs) - set(declared_funcs)) == 0


HANDLERS = {
    list: __handle_list_set_iterable,
    tuple: __handle_tuple,
    dict: __handle_dict,
    set: __handle_list_set_iterable,
    Iterable: __handle_list_set_iterable,
    Union: __handle_union,
    # implicit_union_type: __handle_union,
    Generator: __handle_generator,
    Literal: __handle_literal,
    Callable: __handle_callable,
    Protocol: __handle_protocol,
}


def isoftype(V: Any, T: Any, /, strict: bool = True) -> bool:
    """
    Checks if an object is of a certain type.

    Args:
        V: The object to check.
        T: The type to check against.
        strict: Whether to perform strict type checking.

    Returns:
        True if the object is of the specified type, False otherwise.
    """
    if not isinstance(strict, bool):
        raise TypeError("'strict' must be of type bool")

    obj_origin, obj_args, obj_hints = __isoftype_inquire(V)
    t_origin, t_args, t_hints = __isoftype_inquire(T)

    params = (
        V, T, strict,
        obj_origin, obj_args, obj_hints,
        t_origin, t_args, t_hints
    )

    if t_args is not None and Ellipsis in t_args:
        from ..colors import warning  # pylint: disable=cyclic-import
        warning(
            "using an ellipsis (as in '...') with isoftype is ambiguous returning False")
        return False

    if t_origin is not None:
        if getattr(t_origin, "_is_protocol", False):
            t_origin = Protocol
        if t_origin in HANDLERS:
            if t_origin in (list, tuple, dict, set, dict, Iterable):
                if not isinstance(V, t_origin):
                    return False
            return HANDLERS[t_origin](params)

        from ..colors import warning  # pylint: disable=cyclic-import
        from reflection.interpreter.get_traceback import get_traceback
        warning(
            f"In function isoftype, unhandled t_origin: {t_origin} returning True. stacktrace:")
        print(*get_traceback())
        return True

    return __handle_type_origin(params)


__all__ = [
    "isoftype"
]

__all__ = [
    "isoftype"
]
