from typing import Callable, Any
import functools
from ..Functions import isoneof, isoneof_strict, isoftype
from ..Exceptions import OverloadDuplication, OverloadNotFound
__overload_dict: dict[str, dict[tuple, Callable]] = {}


def overload(*types) -> Callable:
    """decorator for overloading functions\n
    Usage\n-------\n
    @overload(str,str)\n
    def print_info(name,color):
        ...\n\n
    @overload(str,[int,float]))\n
    def print_info(name,age):
        ...\n\n

    * use None to skip argument
    * use no arguments to mark as default function
    * you should overload in decreasing order of specificity! e.g 
    @overload(int) should appear in the code before @overload(Any)

    \n\n\n
    \nRaises:
        OverloadDuplication: if a functions is overloaded twice (or more)
        with same argument types
        OverloadNotFound: if an overloaded function is called with 
        types that has no variant of the function

    \nNotice:
        The function's __doc__ will hold the value of the last variant only
    """
    # make sure to use unique global dictionary
    if len(types) == 1 and type(types[0]).__name__ == "function":
        raise ValueError("can't create an overload without defining types")
    global __overload_dict
    # allow input of both tuples and lists for flexibly
    if len(types) > 0:
        types = list(types)
        for i, maybe_list_of_types in enumerate(types):
            if isoneof(maybe_list_of_types, [list, tuple]):
                types[i] = tuple(sorted(list(maybe_list_of_types),
                                        key=lambda sub_type: sub_type.__name__))
        types = tuple(types)

    def deco(func: Callable) -> Callable:
        if not isinstance(func, Callable):
            raise TypeError("overload decorator must be used on a callable")

        # assign current overload to overload dictionary
        name = f"{func.__module__}.{func.__qualname__}"

        if name not in __overload_dict:
            __overload_dict[name] = {}

        if types in __overload_dict[name]:
            # raise if current overload already exists for current function
            raise OverloadDuplication(
                f"{name} has duplicate overloading for type(s): {types}")

        __overload_dict[name][types] = func

        @ functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            default_func = None
            # select correct overload
            for variable_types, curr_func in __overload_dict[f"{func.__module__}.{func.__qualname__}"].items():
                if len(variable_types) == 0:
                    if default_func is None:
                        default_func = curr_func
                        continue
                    # will not reach here because of duplicate overloading so this is redundant
                    raise ValueError("Can't have two default functions")

                if len(variable_types) != len(args):
                    continue

                for i, variable_type in enumerate(variable_types):
                    if variable_type is not None:
                        if isoneof(variable_type, [list, tuple]):
                            if not isoneof_strict(args[i], variable_type):
                                break
                        else:
                            if not isoftype(args[i], variable_type):
                                break
                else:
                    return curr_func(*args, **kwargs)

            if default_func is not None:
                return default_func(*args, **kwargs)
            # or raise exception if no overload exists for current arguments
            raise OverloadNotFound(
                f"function {func.__module__}.{func.__qualname__} is not overloaded with {[type(v) for v in args]}")

        return wrapper
    return deco


__all__ = [
    "overload"
]
