import inspect
from typing import Optional, Callable
from .callstack import get_prev_frame
from .interpreter import get_python_version

if get_python_version() < (3, 9):
    from typing import Set as t_set  # pylint: disable=ungrouped-imports
else:
    from builtins import set as t_set


def get_caller_name(steps_back: int) -> Optional[str]:
    """returns the name caller of the function

    Returns:
        str: name of caller

    USING THIS FUNCTION WHILE DEBUGGING WILL ADD ADDITIONAL FRAMES TO THE TRACEBACK
    """
    if not isinstance(steps_back, int):
        raise TypeError("steps_back must be an int")
    if steps_back < 0:
        raise ValueError("steps_back must be a non-negative integer")
    if (frame := get_prev_frame(2 + steps_back)) is None:
        return None
    return frame.f_code.co_name


def get_prev_func(steps_back: int) -> Optional[Callable]:
    """Returns the current function"""
    if steps_back < 0:
        raise ValueError("n_step must be a non-negative integer")
    if (caller_frame := get_prev_frame(2 + steps_back)) is None:
        return None
    caller_name = caller_frame.f_code.co_name
    if 'self' in caller_frame.f_locals:
        return getattr(caller_frame.f_locals['self'], caller_name)
    return caller_frame.f_globals.get(caller_name, None)


def get_current_func() -> Optional[Callable]:
    """returns the current func
    Example:
        >>> def foo():
        >>>     return get_current_func()

        >>> foo is foo()
        True
        >>> foo is foo()()()
        True     
    """
    return get_prev_func(1)


def get_caller() -> Optional[Callable]:
    """returns the caller to the current function

    Example:
        >>> def foo():
        >>>     print(get_caller())

        >>> def bar():
        >>>     foo()

        >>> bar()
        "bar"
    """
    return get_prev_func(2)


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


def is_function_annotated_properly(func: Callable, ignore: Optional[set] = None, check_return: bool = True) -> bool:
    """checks whether a function is annotated properly

    Args:
        func (Callable): the function to check
        ignore (set, optional): arguments to ignore when validating.
        when 'None' Defaults to {"self", "cls", "args", "kwargs"}.
        check_return (bool, optional): whether to also check that the return value is annotated. Defaults to True
    Raises:
        ValueError: if any of the parameters is of the wrong type

    Returns:
        bool: result of validation
    """
    from ..functions.isoftype import isoftype
    if not inspect.isfunction(func):
        raise ValueError("param should be a function")

    if ignore is None:
        ignore = {"self", "cls", "args", "kwargs"}
    if not isoftype(ignore, t_set[str]):
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



__all__ = [
    "get_caller_name",
    'get_prev_func',
    "get_current_func",
    'get_caller',
    "get_function_return_type",
    "is_function_annotated_properly",
]
