import logging
from typing import get_args, get_origin, get_type_hints, Any, Union, TypeVar, \
    ForwardRef, Literal, Optional, Protocol, Generic, Type, List, Tuple, Set, Dict
from collections.abc import Callable, Generator, Iterable
from ..reflection import get_python_version
from ..logging_.utils import get_logger
logger = get_logger(__name__)


class _tmp(Protocol): ...


_ProtocolMeta = type(_tmp)
del _tmp

T = TypeVar('T')


class _tmp2(Generic[T]): ...


_GenericAlias = type(_tmp2[int])
del _tmp2, T
cmethod = type(getattr(1, "__lt__"))
try:
    implicit_union_type = type(int | str)
except:
    implicit_union_type = Union

ellipsis_ = ...

PARAMSPEC_STRICT: bool = True
try:
    from typing import ParamSpec
except ImportError:
    PARAMSPEC_STRICT = False


def __isoftype_inquire(obj: Any) -> Tuple[Optional[type], Optional[tuple], Optional[dict]]:
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
    try:
        from typing import Concatenate, ParamSpec
        concatenate_t = type(Concatenate[str, ParamSpec("P_")])
        if get_python_version() < (3, 10):
            if isoftype(t_args[0][0], [ParamSpec, concatenate_t]):
                return True
        else:
            if isoftype(t_args[0], [ParamSpec, concatenate_t]):
                return True
    except ImportError:
        pass

    obj_return_type = obj_hints.get('return')
    obj_param_types = list(obj_hints.values())[:-1] if obj_hints else None
    t_return_type = t_args[1]

    if not PARAMSPEC_STRICT:
        if t_args[0] == Ellipsis:
            return True
        if t_args[0] == [Any]:
            return True

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


def __handle_protocol(params: tuple, /, allow_classes: bool = False) -> bool:
    # TODO is_protocol, _is_runtime_protocol
    from ..reflection import FunctionDeclaration, ClassDeclaration
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params

    if T is Protocol:
        return Protocol in getattr(V, "__mro__", [])
    if T in getattr(V, "__mro__", []):
        return False
    if type(V) == type and type(T) == _GenericAlias and not allow_classes:
        return False
    if type(V) == type and len(t_args) == 0:
        return isinstance(V, T)
    if type(V) != type:
        V = type(V)
    if t_origin is None:
        t_origin = T

    cls = ClassDeclaration.from_cls(t_origin)
    declared_funcs: List[FunctionDeclaration] = list(FunctionDeclaration.get_declared_functions(V))
    required_funcs: List[FunctionDeclaration] = list(FunctionDeclaration.get_declared_functions(t_origin))

    for i, req_func in enumerate(required_funcs):
        if req_func.has_generics:
            if req_func.return_type in req_func.generics:
                new_req_func = req_func.duplicate(
                    return_type=t_args[req_func.generics.index(req_func.return_type)].__name__)
                required_funcs[i] = new_req_func
            for aindex, arg in enumerate(required_funcs[i].arguments):
                for generic in req_func.generics:
                    if arg.type is not None and generic in arg.type:
                        if generic not in cls.generics:
                            return False
                        correct_type = t_args[cls.generics.index(generic)]
                        new_name = correct_type.__name__
                        if new_name == "Union":
                            new_name = str(correct_type).replace("typing.Union", "Union")
                        changed_argument = required_funcs[i].arguments[aindex].duplicate(type=new_name)
                        new_arguments = list(required_funcs[i].arguments)[::]
                        new_arguments[aindex] = changed_argument
                        required_funcs[i] = required_funcs[i].duplicate(arguments=tuple(new_arguments))

    for req in required_funcs:
        for dec in declared_funcs:
            if not len(req.arguments) == len(dec.arguments):
                return False

            if not req.return_type == dec.return_type: return False

            for rarg in req.arguments:
                for darg in dec.arguments:
                    a = rarg.type
                    if a is not None and ("[" in a or "]" in a):
                        a = set([s.strip() for s in a[a.index("[") + 1:a.rindex("]")].split(",")])
                    else:
                        a = set([a])
                    b = darg.type
                    if b is not None and ("[" in b or "]" in b):
                        b = set([s.strip() for s in b[b.index("[") + 1:b.rindex("]")].split(",")])
                    else:
                        b = set([b])
                    if (len(list(b - a))) == 0: break
                else:
                    return False

    return True


def __handle_type(params: tuple) -> bool:
    V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints = params
    if type(V) != type:
        return False
    if t_args[0] in V.__mro__:
        return True
    t_origin, t_args, t_hints = __isoftype_inquire(t_args[0])
    if type(t_origin) is _ProtocolMeta:
        return __handle_protocol((V, T, strict, obj_origin, obj_args, obj_hints, t_origin, t_args, t_hints),
                                 allow_classes=True)
    return False


def __handle_unpack(params: tuple) -> bool:
    # TODO see test_tlist.py -> test_wrong_values ->    with self.assertRaises(TypeError):
    #             tlist[Tuple[int]]([[1], [2], [3], ["4"]])
    raise NotImplemented


HANDLERS: Dict[type, Callable] = {
    list: __handle_list_set_iterable,
    tuple: __handle_tuple,
    dict: __handle_dict,
    set: __handle_list_set_iterable,
    type: __handle_type,
    List: __handle_list_set_iterable,
    Tuple: __handle_tuple,
    Dict: __handle_dict,
    Set: __handle_list_set_iterable,
    Type: __handle_type,
    Iterable: __handle_list_set_iterable,
    Union: __handle_union,
    implicit_union_type: __handle_union,
    Generator: __handle_generator,
    Literal: __handle_literal,
    Callable: __handle_callable,
    Protocol: __handle_protocol,
}
try:
    # This exists only from python version 3.11 onwards
    from typing import Unpack

    HANDLERS[Unpack] = __handle_unpack
except:
    pass


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
        logger.error("'strict' parameter must be of type bool")
        raise TypeError("'strict' must be of type bool")

    obj_origin, obj_args, obj_hints = __isoftype_inquire(V)
    t_origin, t_args, t_hints = __isoftype_inquire(T)

    params = (
        V, T, strict,
        obj_origin, obj_args, obj_hints,
        t_origin, t_args, t_hints
    )

    if t_args is not None and Ellipsis in t_args and PARAMSPEC_STRICT:
        from ..colors import warning  # pylint: disable=cyclic-import
        warning(
            "using an ellipsis (as in '...') with isoftype is ambiguous returning False")
        return False

    if T is Union:
        t_origin = Union  # type:ignore
    elif T is Protocol or Protocol in getattr(T, "__mro__", []):
        t_origin = Protocol  # type:ignore
    elif Protocol in getattr(V, "__mro__", []):
        t_origin = Protocol  # type:ignore

    if t_origin is not None:
        if getattr(t_origin, "_is_protocol", False) or isinstance(t_origin, _ProtocolMeta):
            t_origin = Protocol  # type:ignore

        if t_origin in HANDLERS:
            if t_origin in (list, tuple, dict, set, dict, Iterable):
                if not isinstance(V, t_origin):  # type:ignore
                    return False
            result = HANDLERS[t_origin](params)  # type:ignore
            return result
        # These imports must explicitly be specifically here and not at the top
        logger.warning("Unhandled t_origin: %s, returning True", t_origin)
        from danielutils import warning, get_traceback
        warning(
            f"In function isoftype, unhandled t_origin: {t_origin} returning True. stacktrace:")
        print(*get_traceback())
        return True

    result = __handle_type_origin(params)
    return result


__all__ = [
    "isoftype"
]
