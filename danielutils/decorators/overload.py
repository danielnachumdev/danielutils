from typing import Callable, cast, Any, TypeVar, Dict as t_dict, List as t_list
import inspect
import functools
from ..reflection import is_function_annotated_properly
from ..functions import isoftype, isoneof, isoneof_strict
from ..exceptions import OverloadDuplication, OverloadNotFound
from .deprecate import deprecate
from ..reflection import get_python_version

if get_python_version() < (3, 9):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec  # type:ignore# pylint: disable=ungrouped-imports
    from builtins import dict as t_dict, list as t_list
T = TypeVar("T")
P = ParamSpec("P")
FuncT = Callable[P, T]  # type:ignore
T2 = TypeVar("T2")
P2 = ParamSpec("P2")
FuncT2 = Callable[P2, T2]  # type:ignore

__overload_dict: t_dict[str, t_dict[tuple, Callable]] = {}


@deprecate("'explicit_global_overload' is a legacy decorator please use 'overload' instead")
def explicit_global_overload(*types) -> Callable:
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
    types = cast(tuple, types)
    # allow input of both tuples and lists for flexibly
    if len(types) > 0:
        types_as_list = list(types)
        for i, maybe_list_of_types in enumerate(types):
            if isoneof(maybe_list_of_types, [list, tuple]):
                types_as_list[i] = tuple(sorted(list(maybe_list_of_types),
                                                key=lambda sub_type: sub_type.__name__))
        types = tuple(types_as_list)

    def deco(func: Callable) -> Callable:
        if not callable(func):
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

        @functools.wraps(func)
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


class overload:
    """this class create an object to manage the overloads for a given function.\n
    will only match a specific resolution and won't infer best guess for types
    """

    __SKIP_SET = {"self", "cls", "args", "kwargs"}

    def __init__(self, func: FuncT):
        overload._validate(func)
        self._qualname = func.__qualname__
        self._moudle = func.__module__
        self._functions: t_dict[int, t_list[Callable]] = {}
        self._functions[overload._get_key(func)] = [func]
        functools.wraps(func)(self)

    @staticmethod
    def _get_key(func: Callable):
        return len(inspect.signature(func).parameters)

    @staticmethod
    def _validate(func: Callable):
        if not callable(func):
            raise ValueError("Can only overload functions")
        if not is_function_annotated_properly(func):
            raise ValueError(
                f"{func.__module__}.{func.__qualname__} is not properly annotated."
                "\nFunction must be fully annotated to be overloaded")

    def overload(self, func: FuncT2) -> "overload":
        """will add another function to the list of available options

        Args:
            func (Callable): a new alternative function

        Returns:
            overload2: returns the overload object
        """
        self._validate(func)
        k = overload._get_key(func)
        if k not in self._functions:
            self._functions[k] = []
        self._functions[k].append(func)
        return self

    def __call__(self, *args, **kwargs):
        num_args = len(args) + len(kwargs.keys())
        if num_args not in self._functions:
            raise AttributeError(
                f"No overload with {num_args} argument found for {self._moudle}.{self._qualname}")

        if num_args == 0:
            return self._functions[num_args][0](*args, **kwargs)

        max_score = 0
        winner = self._functions[num_args][0]
        EXACT_MATCH = 1 / num_args
        SUBCLASS = 1 / num_args
        for func in self._functions[num_args]:
            score = 0
            signature = inspect.signature(func)
            for i, tup in enumerate(signature.parameters.items()):
                param_name, param_type = tup
                if param_name in overload.__SKIP_SET:
                    continue

                if type(args[i]) == param_type.annotation:  # pylint :disable=unidiomatic-typecheck
                    score += EXACT_MATCH

                elif isoftype(args[i], param_type.annotation):
                    score += SUBCLASS
                else:
                    break

            else:
                # reaching here means current function matches perfectly the annotation
                if score > max_score:
                    max_score = score
                    winner = func
        # raise AttributeError("No overload found")

        return winner(*args, **kwargs)


__all__ = [
    "explicit_global_overload",
    "overload"
]
