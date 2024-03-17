import inspect
from typing import cast, Optional, Callable, Any
from types import FrameType
from .get_prev_frame import get_prev_frame_from, get_n_prev_frame
from ..reflection import get_python_version

if get_python_version() < (3, 9):
    from typing import List as t_list, Set as t_set  # pylint: disable=ungrouped-imports
else:
    from builtins import list as t_list, set as t_set


def get_caller_name(steps_back: int = 0) -> Optional[str]:
    """returns the name caller of the function

    Returns:
        str: name of caller

    USING THIS FUNCTION WHILE DEBUGGING WILL ADD ADDITIONAL FRAMES TO THE TRACEBACK
    """
    if not isinstance(steps_back, int):
        raise TypeError("steps_back must be an int")
    if steps_back < 0:
        raise ValueError("steps_back must be a non-negative integer")
    if (frame := get_n_prev_frame(2)) is None:
        return None
    frame = cast(FrameType, frame)
    while steps_back > 0:
        if (frame := cast(FrameType, get_prev_frame_from(frame))) is None:
            return None
        steps_back -= 1
    return frame.f_code.co_name


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


def get_current_func():
    caller_frame = get_n_prev_frame(2)
    caller_name = caller_frame.f_code.co_name
    caller_func = caller_frame.f_globals[caller_name]
    return caller_func


def get_caller_func() -> Optional[Callable]:
    caller_frame = get_n_prev_frame(3)
    if (caller_name := caller_frame.f_code.co_name) == "<module>":
        return None
    caller_func = caller_frame.f_globals[caller_name]
    return caller_func


import json


def get_n_caller_func(n_steps: int = 1) -> Optional[Callable]:
    caller_frame = get_n_prev_frame(2 + n_steps)
    # print(json.dumps(dict(caller_frame.f_globals), default=str, indent=4))
    if (caller_name := caller_frame.f_code.co_name) == "<module>":
        return None
    caller_func = caller_frame.f_globals[caller_name]
    return caller_func


def get_caller_module_name() -> Optional[str]:
    caller_func = get_caller_func()
    if caller_func is None:
        return None
    return caller_func.__module__


def get_mro(obj: Any) -> t_list[type]:
    """returns the mro of an object

    Args:
        obj (Any): any object, instance or class

    Returns:
        list[type]: the resulting mro for the object
    """
    if isinstance(obj, type):
        return obj.mro()
    return get_mro(obj.__class__)


__all__ = [
    "get_caller_name",
    "get_function_return_type",
    "is_function_annotated_properly",
    "get_mro",
    "get_current_func",
    "get_caller_func",
    "get_n_caller_func",
    "get_caller_module_name"
]
