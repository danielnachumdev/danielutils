from __future__ import annotations
from typing import Callable, Any, Optional
import inspect
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


def is_function_annotated_properly(func: Callable, ignore: Optional[set] = None, check_return: bool = True) -> bool:
    """checks wheter a function is annotated properly

    Args:
        func (Callable): the function to check
        ignore (set, optional): arguments to ignore when validating. when 'None' Defaults to {"self", "cls", "args", "kwargs"}.
        check_return (bool, optional): whether to also check that the return value is annotated. Defaults to True
    Raises:
        ValueError: if any of the parameters is of the wrong type

    Returns:
        bool: result of validation
    """

    if not inspect.isfunction(func):
        raise ValueError("param should be a function")

    if ignore is None:
        ignore = {"self", "cls", "args", "kwargs"}
    if not isoftype(ignore, set[str]):
        raise ValueError("ignore must be a set of str")

    # get the signature of the function
    signature = inspect.signature(func)
    for arg_name, arg_param in signature.parameters.items():
        if arg_name not in ignore:
            arg_type = arg_param.annotation
            # check if an annotation is missing
            if arg_type == inspect.Parameter.empty:
                return False
        # check if the argument has a default value
        default_value = signature.parameters[arg_name].default
        if default_value != inspect.Parameter.empty:
            # allow everything to be set to None as default
            if default_value is None:
                continue
            # if it does, check the type of the default value
            if not isoftype(default_value, arg_type):
                return False

    if check_return:
        pass
    return True


class overload2:
    """this class create an object to manage the overloads for a given function.\n
    will only match a specific resolution and won't infer best guess for types
    """

    SKIP_SET = {"self", "cls", "args", "kwargs"}

    def __init__(self, func):
        overload2._validate(func)
        self.qualname = func.__qualname__
        self.moudle = func.__module__
        self.functions: dict[int, list[Callable]] = dict()
        self.functions[overload2._get_key(func)] = [func]

    @staticmethod
    def _get_key(func):
        return len(inspect.signature(func).parameters)

    @staticmethod
    def _validate(func):
        if not isinstance(func, Callable):
            raise ValueError("Can only overload functions")
        if not is_function_annotated_properly(func):
            raise ValueError(
                "Function must be fully annotated to be overloaded")

    def prepare_for_wraps(self):
        return next(iter(self.functions.values()))[0]

    def overload(self, func: Callable) -> overload2:
        """will add another function to the list of available options

        Args:
            func (Callable): a new alternative function

        Returns:
            overload2: returns the overload object
        """
        self._validate(func)
        k = overload2._get_key(func)
        if k not in self.functions:
            self.functions[k] = []
        self.functions[k].append(func)
        return self

    def __call__(self, *args, **kwargs):
        num_args = len(args)+len(kwargs.keys())
        if num_args not in self.functions:
            raise AttributeError(
                f"No overload with {num_args} argument found for {self.moudle}.{self.qualname}")
        selected_func = None
        if len(self.functions[num_args]) == 1:
            selected_func = self.functions[num_args][0]
        else:
            for func in self.functions[num_args]:
                signature = inspect.signature(func)
                for i, tup in enumerate(signature.parameters.items()):
                    param_name, param_type = tup
                    if param_name in overload2.SKIP_SET:
                        continue

                    if not isoftype(args[i], param_type.annotation):
                        break
                else:
                    # reaching here means current function matches perfectly the annotation
                    selected_func = func
                    break
            else:
                raise AttributeError("No overload found")

        return selected_func(*args, **kwargs)


class OverloadMeta(type):
    @staticmethod
    def overload(func: Callable) -> overload2:
        return overload2(func)

    def __new__(mcs, name, bases, namespace):
        # og_getattribute = None
        # if "__getattribute__" in namespace:
        #     og_getattribute = namespace["__getattribute__"]

        # def __getattribute__(self, name: str) -> Any:
        #     if not hasattr(type(self), name):
        #         if og_getattribute:
        #             return og_getattribute(self, name)
        #         return object.__getattribute__(self, name)

        #     function_obj: OverloadMeta.overload = getattr(
        #         type(self), name)

        #     @functools.wraps(function_obj)
        #     def wrapper(*args, **kwargs):
        #         return function_obj(self, *args, **kwargs)

        #     return wrapper

        def create_wrapper(v: overload2):
            @functools.wraps(v.prepare_for_wraps())
            def wrapper(*args, **kwargs):
                return v(*args, **kwargs)
            return wrapper

        for k, v in namespace.items():
            if isinstance(v, overload2):
                namespace[k] = create_wrapper(v)
        # namespace["__getattribute__"] = __getattribute__

        return super().__new__(mcs, name, bases, namespace)


__all__ = [
    "overload",
    "OverloadMeta"
]
