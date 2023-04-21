import re
import traceback
import functools
import inspect
import threading
from typing import Callable, Any, get_type_hints
import sys
from .Functions import isoneof, isoneof_strict, isoftype
from .Exceptions import *


def validate(strict: Callable | bool = True) -> Callable:
    """A decorator that validates the annotations and types of the arguments and return
    value of a function.

        * 'None' is allowed as default value for everything
        * Because of their use in classes, the generally accepted keywords 'self' and 'cls'
        are not validated to not break intellisense when using 'Any'

    Args:
        func (Callable): The function to be decorated.

    Raises:
        TypeError: if the decorated object is nto a Callable
        EmptyAnnotationException: If an argument is not annotated.
        InvalidDefaultValueException: If an argument's default value is not of the annotated type.
        ValidationException: If an argument's value is not of the expected type.
        InvalidReturnValueException: If the return value is not of the expected type.

    Returns:
        Callable: A wrapper function that performs the validation and calls the original function.
    """
    if not isoftype(strict, bool | Callable):
        raise TypeError(
            "the argument for validate must be a Callable or a boolean to mark strict use")

    def deco(func):
        nonlocal strict
        SKIP_SET = {"self", "cls"}
        if not isinstance(func, Callable):
            raise TypeError(
                "The validate decorator must only decorate a function")
        func_name = f"{func.__module__}.{func.__qualname__}"
        # get the signature of the function
        signature = inspect.signature(func)
        for arg_name, arg_param in signature.parameters.items():
            if arg_name not in SKIP_SET:
                arg_type = arg_param.annotation
                # check if an annotation is missing
                if arg_type == inspect.Parameter.empty:
                    raise EmptyAnnotationException(
                        f"In {func_name}, argument '{arg_name}' is not annotated")

            # check if the argument has a default value
            default_value = signature.parameters[arg_name].default
            if default_value != inspect.Parameter.empty:
                # allow everything to be set to None as default
                if default_value is None:
                    continue
                # if it does, check the type of the default value
                if not isoftype(default_value, arg_type):
                    raise InvalidDefaultValueException(
                        f"In {func_name}, argument '{arg_name}'s default value is annotated \
                        as {arg_type} but got '{default_value}' which is {type(default_value)}")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            """wrapper function for the type validating - will run on each call independently
            """
            hints = None
            # check all arguments
            bound = signature.bind(*args, **kwargs)
            for variable_name, variable_value in bound.arguments.items():
                if variable_name in SKIP_SET:
                    continue
                expected_type = func.__annotations__[variable_name]

                if isinstance(expected_type, str):
                    # why does this even happen?
                    if hints is None:
                        hints = get_type_hints(func)
                    expected_type = hints[variable_name]

                if not isoftype(variable_value, expected_type, strict=strict):
                    raise ValidationException(
                        f"In {func_name}, argument '{variable_name}' is annotated as \
                            {expected_type} but got '{variable_value}' which is {type(variable_value)}")

            # call the function
            result = func(*args, **kwargs)

            # check the return type
            return_type = type(None) if ("inspect._empty" in str(signature.return_annotation)
                                         or signature.return_annotation is None) else signature.return_annotation
            if isinstance(return_type, str):
                # why does this even happen?
                return_type = get_type_hints(func)["return"]
            if return_type is not type(None) and not isoftype(result, return_type):
                raise InvalidReturnValueException(
                    f"In function {func_name}, the return type is annotated as "
                    f"{return_type} but got '{result}' which is {type(result)}")
            return result
        return wrapper
    if isinstance(strict, Callable):
        func = strict
        strict = True
        return deco(func)
    return deco
    # this means that strict is actually the function

# def validate(func: Callable) -> Callable:
    # """A decorator that validates the annotations and types of the arguments and return
    # value of a function.

    #     * 'None' is allowed as default value for everything
    #     * Because of their use in classes, the generally accepted keywords 'self' and 'cls'
    #     are not validated to not break intellisense when using 'Any'

    # Args:
    #     func (Callable): The function to be decorated.

    # Raises:
    #     TypeError: if the decorated object is nto a Callable
    #     EmptyAnnotationException: If an argument is not annotated.
    #     InvalidDefaultValueException: If an argument's default value is not of the annotated type.
    #     ValidationException: If an argument's value is not of the expected type.
    #     InvalidReturnValueException: If the return value is not of the expected type.

    # Returns:
    #     Callable: A wrapper function that performs the validation and calls the original function.
    # """
    # SKIP_SET = {"self", "cls"}
    # if not isinstance(func, Callable):
    #     raise TypeError("The validate decorator must only decorate a function")
    # func_name = f"{func.__module__}.{func.__qualname__}"
    # # get the signature of the function
    # signature = inspect.signature(func)
    # for arg_name, arg_param in signature.parameters.items():
    #     if arg_name not in SKIP_SET:
    #         arg_type = arg_param.annotation
    #         # check if an annotation is missing
    #         if arg_type == inspect.Parameter.empty:
    #             raise EmptyAnnotationException(
    #                 f"In {func_name}, argument '{arg_name}' is not annotated")

    #     # check if the argument has a default value
    #     default_value = signature.parameters[arg_name].default
    #     if default_value != inspect.Parameter.empty:
    #         # allow everything to be set to None as default
    #         if default_value is None:
    #             continue
    #         # if it does, check the type of the default value
    #         if not isoftype(default_value, arg_type):
    #             raise InvalidDefaultValueException(
    #                 f"In {func_name}, argument '{arg_name}'s default value is annotated \
    #                 as {arg_type} but got '{default_value}' which is {type(default_value)}")

    # @functools.wraps(func)
    # def wrapper(*args, **kwargs):
    #     """wrapper function for the type validating - will run on each call independently
    #     """
    #     hints = None
    #     # check all arguments
    #     bound = signature.bind(*args, **kwargs)
    #     for variable_name, variable_value in bound.arguments.items():
    #         if variable_name in SKIP_SET:
    #             continue
    #         expected_type = func.__annotations__[variable_name]

    #         if isinstance(expected_type, str):
    #             # why does this even happen?
    #             if hints is None:
    #                 hints = get_type_hints(func)
    #             expected_type = hints[variable_name]

    #         if not isoftype(variable_value, expected_type):
    #             raise ValidationException(
    #                 f"In {func_name}, argument '{variable_name}' is annotated as \
    #                     {expected_type} but got '{variable_value}' which is {type(variable_value)}")

    #     # call the function
    #     result = func(*args, **kwargs)

    #     # check the return type
    #     return_type = type(None) if ("inspect._empty" in str(signature.return_annotation)
    #                                  or signature.return_annotation is None) else signature.return_annotation
    #     if isinstance(return_type, str):
    #         # why does this even happen?
    #         return_type = get_type_hints(func)["return"]
    #     if return_type is not type(None) and not isoftype(result, return_type):
    #         raise InvalidReturnValueException(
    #             f"In function {func_name}, the return type is annotated as "
    #             f"{return_type} but got '{result}' which is {type(result)}")
    #     return result
    # return wrapper

# @validate
# def NotImplemented(func: Callable) -> Callable:
#     """decorator to mark function as not implemented for development purposes

#     Args:
#         func (Callable): the function to decorate
#     """
#     @ functools.wraps(func)
#     def wrapper(*args, **kwargs) -> Any:
#         raise NotImplementedError(
#             f"As marked by the developer {func.__module__}.{func.__qualname__} is not implemented yet..")
#     return wrapper


@validate
def PartiallyImplemented(func: Callable) -> Callable:
    """decorator to mark function as not fully implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    from .Colors import warning

    @ functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        warning(
            f"As marked by the developer, {func.__module__}.{func.__qualname__} "
            "may not be fully implemented and might not work properly.")
        return func(*args, **kwargs)
    return wrapper


@validate
def memo(func: Callable) -> Callable:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: dict[tuple, Any] = {}

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return cache[(args, *kwargs.items())]
    return wrapper


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


@validate
def abstractmethod(func: Callable) -> Callable:
    """A decorator to mark a function to be 'pure virtual' / 'abstract'

    Args:
        func (Callable): the function to mark

    Raises:
        NotImplementedError: the error that will rise when the marked function
        will be called if not overridden in a derived class
    """
    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"{func.__module__}.{func.__qualname__} MUST be overridden in a child class")
    return wrapper


# __virtualization_tables = {}


# @NotImplemented
# def virtual(func: Callable) -> Callable:
#     def wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper


# @NotImplemented
# def override(func: Callable) -> Callable:
#     def wrapper(*args, **kwargs):
#         return func(*args, **kwargs)
#     return wrapper


# @ PartiallyImplemented
# @validate
# def deprecate(obj:  Callable) -> Callable:
#     """decorator to mark function as deprecated

#     Args:
#         obj (Union[str, None, Callable], optional): Defaults to None.

#         Can operate in two configurations:\n
#         1. obj is the function that you want to deprecate\n
#         \t@deprecate\n
#         \tdef foo(...):\n
#         \t\t...\n\n
#         2. obj is an advise message\n
#         \t@deprecate("instead use ...")\n
#         \tdef foo(...):
#         \t\t...
#     """
#     from .Colors import warning
#     # if callable(obj):
#     if isinstance(obj, Callable):
#         @ functools.wraps(obj)
#         def wrapper(*args, **kwargs) -> Any:
#             warning(
#                 f"As marked by the developer, {obj.__module__}.{obj.__qualname__} is deprecated")
#             return obj(*args, **kwargs)
#         return wrapper

#     def deco(func: Callable) -> Callable:
#         @ functools.wraps(func)
#         def wrapper(*args, **kwargs) -> Any:
#             warning(
#                 f"As marked by the developer, {func.__module__}.{func.__qualname__} is deprecated")
#             if obj:
#                 print(obj)
#             return func(*args, **kwargs)
#         return wrapper
#     return deco


@validate
def atomic(func: Callable) -> Callable:
    """will make function thread safe by making it
    accessible for only one thread at one time

    Args:
        func (Callable): function to make thread safe

    Returns:
        Callable: the thread safe function
    """
    lock = threading.Lock()

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper


@validate
def limit_recursion(max_depth: int, return_value: Any = None, quiet: bool = True):
    """decorator to limit recursion of functions

    Args:
        max_depth (int): max recursion depth which is allowed for this function
        return_value (_type_, optional): The value to return when the limit is reached. Defaults to None.
            if is None, will return the last (args, kwargs)
        quiet (bool, optional): whether to print a warning message. Defaults to True.
    """

    from .Colors import warning

    def deco(func):
        @ functools.wraps(func)
        def wrapper(*args, **kwargs):
            depth = functools.reduce(
                lambda count, line:
                    count + 1 if re.search(rf"{func.__name__}\(.*\)$", line)
                    else count,
                traceback.format_stack(), 0
            )
            if depth >= max_depth:
                if not quiet:
                    warning(
                        "limit_recursion has limited the number of calls for "
                        f"{func.__module__}.{func.__qualname__} to {max_depth}")
                if return_value:
                    return return_value
                return args, kwargs
            return func(*args, **kwargs)
        return wrapper
    return deco


@validate
def timeout(duration: int | float) -> Callable:
    """A decorator to limit runtime for a function

    Args:
        duration (int | float): allowed runtime duration

    Raises:
        thread_error: if there is a thread related error
        function_error: if there is an error in the decorated function

    Returns:
        Callable: The decorated function
    """
    # https://stackoverflow.com/a/21861599/6416556
    def timeout_deco(func: Callable) -> Callable:
        if not isinstance(func, Callable):
            raise ValueError("timeout must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [
                TimeoutError(f'{func.__module__}.{func.__qualname__} timed out after {duration} seconds!')]

            def timeout_wrapper() -> None:
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as function_error:
                    res[0] = function_error

            t = threading.Thread(target=timeout_wrapper, daemon=True)
            try:
                t.start()
                t.join(duration)
            except Exception as thread_error:
                raise thread_error
            if isinstance(res[0], BaseException):
                raise res[0]
            return res[0]
        return wrapper
    return timeout_deco


@validate
def attach(before: Callable = None, after: Callable = None) -> Callable:
    """attaching functions to a function

    Args:
        before (Callable, optional): function to call before. Defaults to None.
        after (Callable, optional): function to call after. Defaults to None.

    Raises:
        ValueError: if both before and after are none
        ValueError: if the decorated object is not a Callable

    Returns:
        Callable: the decorated result
    """
    if before is None and after is None:
        raise ValueError("You must supply at least one function")

    def attach_deco(func: Callable):
        if not isinstance(func, Callable):
            raise ValueError("attach must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if before is not None:
                before()
            res = func(*args, **kwargs)
            if after is not None:
                after()
            return res
        return wrapper
    return attach_deco


@validate(strict=False)
def decorate_conditionally(decorator: Callable, predicate: bool | Callable[[], bool], args: list = None):
    """will decorate a function iff the predicate is True or returns True

    Args:
        decorator (Callable): the decorator to use
        predicate (bool | Callable[[], bool]): the predicate
    """

    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        if (predicate() if isinstance(predicate, Callable) else predicate):
            if args is None:
                return decorator(func)
            return decorator(*args)(func)
        return wrapper
    return deco


__all__ = [
    "validate",
    # "NotImplemented",
    "PartiallyImplemented",
    "memo",
    "overload",
    "abstractmethod",
    # "virtual",
    # "override",
    # "deprecate",
    "atomic",
    "limit_recursion",
    "timeout",
    "attach",
    "decorate_conditionally"

]
