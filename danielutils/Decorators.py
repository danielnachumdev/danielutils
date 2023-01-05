from .Typing import Callable, Type, Any, Union, Tuple
import functools
import threading
from .Functions import areoneof, isoneof, isoneof_strict, isoftype
from .Exceptions import OverloadDuplication, OverloadNotFound, ValidationTypeError, ValidationValueError, ValidationReturnTypeError, TimeoutError
__validation_set = set()
__validation_instantiation_rule = dict()


def __validate_type(func: Callable, v: Any, T: Type, validation_func: Callable[[Any], bool] = isoftype, msg: str = None) -> None:
    if not validation_func(v, T):
        raise ValidationTypeError(
            msg or f"In {func.__module__}.{func.__qualname__}(...)\nThe argument is: '{ v.__qualname__ if hasattr(v, '__qualname__') else v}'\nIt has the type of '{type(v)}'\nIt is marked as type(s): '{T}'")


def __validate_condition(func: Callable, v: Any, constraint: Callable[[Any], bool], msg: str = None) -> None:
    if not constraint(v):
        raise ValidationValueError(
            msg or f"In {func.__module__}.{func.__qualname__}(...)\nThe argument '{str(v)}' has failed provided constraint\nConstraint in {constraint.__module__}.{constraint.__qualname__}")


def __validate_arg(func: Callable, curr_arg: Any, curr_inner_arg: Any) -> None:
    if isoneof(curr_arg, [list, Tuple]):
        # multiple type only:
        if areoneof(curr_arg, [Type]):
            __validate_type(func, curr_inner_arg, curr_arg, isoneof)

        else:  # maybe with condition:
            class_type, constraint = curr_arg[0], curr_arg[1]

            # Type validation
            if isoneof(class_type, [list, Tuple]):
                __validate_type(func, curr_inner_arg, class_type, isoneof)
            else:
                __validate_type(func, curr_inner_arg, class_type, isinstance)

            # constraints validation
            if constraint is not None:
                message = curr_arg[2] if len(curr_arg) > 2 else None
                __validate_condition(func, curr_inner_arg, constraint, message)
    else:
        __validate_type(func, curr_inner_arg, curr_arg)


def validate(*args, return_type=None, can_instantiate_multiple_times: bool = False) -> Callable:
    """validate decorator

        Is passed types of variables to perform type checking over\n
        The arguments must be passed in the same order\n

    for each parameter respectively you can choose one of four options:\n
        1. None - to skip\n
        2. Type - a type to check \n
        3. Sequence of Type to check if the type is contained in the sequence\n
        4. Sequence that contains three arguments:\n
            4.1 a Type or Sequence[Type]\n
            4.2 a function to call on argument\n
            4.3 a str to display in a ValueError iff the condition from 4.2 fails\n
    In addition you can use keyword 'return_type' for the returned value same as specified in 1,2,3
    """
    from .Exceptions import ValidationDuplicationError, ValidationTypeError, ValidationValueError, ValidationReturnTypeError

    def wrapper(func: Callable) -> Callable:
        global __validation_set, __validation_instantiation_rule
        func_id = f"{func.__module__}.{func.__qualname__}"

        if func_id not in __validation_instantiation_rule:
            __validation_instantiation_rule[func_id] = can_instantiate_multiple_times
        assert can_instantiate_multiple_times == __validation_instantiation_rule[
            func_id], "can't change instantiation status on runtime"

        if func_id not in __validation_set:
            __validation_set.add(func_id)
        else:
            if not __validation_instantiation_rule[func_id]:
                raise ValidationDuplicationError(
                    "validate decorator is being used on two functions in the same module with the same name\nmaybe use @overload instead")

        @ functools.wraps(func)
        def inner(*inner_args, **inner_kwargs) -> Any:
            for i in range(min(len(args), len(inner_args))):
                if args[i] is not None:
                    __validate_arg(func, args[i], inner_args[i])
            res = func(*inner_args, **inner_kwargs)
            if return_type is not None:
                msg = f"In {func.__module__}.{func.__qualname__}(...)\nThe returned value is: '{ res.__qualname__ if hasattr(res, '__qualname__') else res}'\nIt has the type of '{type(res)}'\nIt is marked as type(s): '{return_type}'"
                __validate_type(func, res, return_type, msg=msg)
            return res
        return inner
    return wrapper


@ validate(Callable)
def NotImplemented(func: Callable) -> Callable:
    """decorator to mark function as not implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    @ functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        raise NotImplementedError(
            f"As marked by the developer {func.__module__}.{func.__qualname__} is not implemented yet..")
    return wrapper


@ validate(Callable)
def PartiallyImplemented(func: Callable) -> Callable:
    """decorator to mark function as not fully implemented for development purposes

    Args:
        func (Callable): the function to decorate
    """
    from .Colors import warning

    @ functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        warning(
            f"As marked by the developer, {func.__module__}.{func.__qualname__} may not be fully implemented and might not work properly")
        return func(*args, **kwargs)
    return wrapper


@ validate(Callable)
def memo(func: Callable) -> Callable:
    """decorator to memorize function calls in order to improve performance by using more memory

    Args:
        func (Callable): function to memorize
    """
    cache: dict[Tuple, Any] = {}

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        if (args, *kwargs.items()) not in cache:
            cache[(args, *kwargs.items())] = func(*args, **kwargs)
        return cache[(args, *kwargs.items())]
    return wrapper


__overload_dict: dict[str, dict[Tuple, Callable]] = dict()


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
    * you should overload in decreasing order of specificity! e.g @overload(int) should appear in the code before @overload(Any)

    \n\n\n
    \nRaises:
        OverloadDuplication: if a functions is overloaded twice (or more) with same argument types
        OverloadNotFound: if an overloaded function is called with types that has no variant of the function

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
            if isoneof(maybe_list_of_types, [list, Tuple]):
                types[i] = tuple(sorted(list(maybe_list_of_types),
                                        key=lambda sub_type: sub_type.__name__))
        types = tuple(types)

    def wrapper(func: Callable) -> Callable:
        if not isinstance(func, Callable):
            raise TypeError("overload decorator must be used on a callable")

        # assign current overload to overload dictionary
        name = f"{func.__module__}.{func.__qualname__}"

        if name not in __overload_dict:
            __overload_dict[name] = dict()

        if types in __overload_dict[name]:
            # raise if current overload already exists for current function
            raise OverloadDuplication(
                f"{name} has duplicate overloading for type(s): {types}")

        __overload_dict[name][types] = func

        @ functools.wraps(func)
        def inner(*args, **kwargs) -> Any:
            default_func = None
            # select correct overload
            for variable_types, curr_func in __overload_dict[f"{func.__module__}.{func.__qualname__}"].items():
                if len(variable_types) == 0:
                    if default_func is None:
                        default_func = curr_func
                        continue
                    else:
                        # will not reach here because of duplicate overloading so this is redundant
                        raise ValueError("Can't have two default functions")

                if len(variable_types) != len(args):
                    continue

                for i, variable_type in enumerate(variable_types):
                    if variable_type is not None:
                        if isoneof(variable_type, [list, Tuple]):
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

        return inner
    return wrapper


@ validate(Callable)
def abstractmethod(func: Callable) -> Callable:
    """A decorator to mark a function to be 'pure virtual' / 'abstract'

    Args:
        func (Callable): the function to mark

    Raises:
        NotImplementedError: the error that will rise when the marked function will be called if not overridden in a derived class
    """
    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        raise NotImplementedError(
            f"{func.__module__}.{func.__qualname__} MUST be overrided in a child class")
    return wrapper


purevirtual = abstractmethod

# __virtualization_tables = dict()


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


@ PartiallyImplemented
@ validate([str, Callable])
def deprecate(obj: Union[str, Callable] = None) -> Callable:
    """decorator to mark function as deprecated

    Args:
        obj (Union[str, None, Callable], optional): Defaults to None.

        Can operate in two configurations:\n
        1. obj is the function that you want to deprecate\n
        \t@deprecate\n
        \tdef foo(...):\n
        \t\t...\n\n
        2. obj is an advise message\n
        \t@deprecate("instead use ...")\n
        \tdef foo(...):
        \t\t...
    """
    from .Colors import warning
    # if callable(obj):
    if isinstance(obj, Callable):
        @ functools.wraps(obj)
        def inner(*args, **kwargs) -> Any:
            warning(
                f"As marked by the developer, {obj.__module__}.{obj.__qualname__} is deprecated")
            return obj(*args, **kwargs)
        return inner

    def wrapper(func: Callable) -> Callable:
        @ functools.wraps(func)
        def inner(*args, **kwargs) -> Any:
            warning(
                f"As marked by the developer, {func.__module__}.{func.__qualname__} is deprecated")
            if obj:
                print(obj)
            return func(*args, **kwargs)
        return inner
    return wrapper


@ validate(Callable)
def atomic(func):
    import threading
    lock = threading.Lock()

    @ functools.wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    return wrapper


@ validate([int, lambda d: d > 0, "limit_recursion's max_depth must be a positive integer"], None, bool)
def limit_recursion(max_depth: int, return_value=None, quiet: bool = True):
    """decorator to limit recursion of functions

    Args:
        max_depth (int): max recursion depth which is allowed for this function
        return_value (_type_, optional): The value to return when the limit is reached. Defaults to None.
            if is None, will return the last (args, kwargs)
        quiet (bool, optional): whether to print a warning message. Defaults to True.
    """
    import traceback
    import re
    from .Colors import warning

    def wrapper(func):
        @ functools.wraps(func)
        def inner(*args, **kwargs):
            depth = functools.reduce(
                lambda count, line:
                    count + 1 if re.search(f"{func.__name__}\(.*\)$", line)
                    else count,
                traceback.format_stack(), 0
            )
            if depth >= max_depth:
                if not quiet:
                    warning(
                        f"limit_recursion has limited the number of calls for {func.__module__}.{func.__qualname__} to {max_depth}")
                if return_value:
                    return return_value
                return args, kwargs
            return func(*args, **kwargs)
        return inner
    return wrapper


@validate([int, float])
def timeout(timeout: float) -> Callable:
    """WILL NOT WORK WHEN DEBUGGING

    Args:
        timeout (float): seconds to wait until forced timeout

    Raises:
        thread_error: any internal error from the target
        res: TimeoutError

    Returns:
        Callable: decorated function
    """
    # https://stackoverflow.com/a/21861599/6416556
    def timeout_deco(func: Callable) -> Callable:
        if not isinstance(func, Callable):
            raise ValueError("timeout must decorate a function")

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            res = [
                TimeoutError(f'{func.__module__}.{func.__qualname__} timed out after {timeout} seconds!')]

            def timeout_wrapper() -> None:
                try:
                    res[0] = func(*args, **kwargs)
                except Exception as function_error:
                    res[0] = function_error

            t = threading.Thread(target=timeout_wrapper, daemon=True)
            try:
                t.start()
                t.join(timeout)
            except Exception as thread_error:
                raise thread_error
            if isinstance(res[0], BaseException):
                raise res[0]
            return res[0]
        return wrapper
    return timeout_deco


@validate(Callable, Callable)
def attach(before: Callable = None, after: Callable = None) -> Callable:
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


__all__ = [
    "validate",
    "NotImplemented",
    "PartiallyImplemented",
    "memo",
    "overload",
    "abstractmethod",
    "purevirtual",
    # "virtual",
    # "override",
    "deprecate",
    "atomic",
    "limit_recursion",
    "timeout",
    "attach"
]
