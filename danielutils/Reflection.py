import inspect
import traceback
import platform
import sys
import importlib
from enum import Enum
from typing import Any, Callable


def get_caller_name(steps_back: int = 0) -> str:
    """returns the name caller of the function

    Returns:
        str: name of caller
    """
    if not isinstance(steps_back, int):
        raise TypeError("steps_back must be an int")
    if not steps_back >= 0:
        raise ValueError("steps_back must be a non-negative integer")
    # different implementation:

    # RGX = r'File ".*", line \d+, in (.+)\n'
    # # traceback_list = get_traceback()
    # # callee_frame = traceback_list[-1]
    # # callee_name = re.search(RGX, callee_frame).group(1)
    # # caller_frame = traceback_list[-2]
    # # caller_name = re.search(RGX, caller_frame).group(1)

    # this is more readable:

    # current_frame = inspect.currentframe()
    # callee_frame = current_frame.f_back
    # # callee_name = callee_frame.f_code.co_name
    # caller_frame = callee_frame.f_back
    # caller_name = caller_frame.f_code.co_name
    # return caller_name
    frame = inspect.currentframe().f_back.f_back
    while steps_back > 0:
        frame = frame.f_back
        steps_back -= 1
    return frame.f_code.co_name


def dynamically_load(module_name: str, obj_name: str) -> Any:
    """dynammically loads the module and returns the object from this file

    Args:
        module_name (str): name of python module, (typically a file name without extention)
        obj_name (str): the name of the wanted object

    Returns:
        Any: the object
    """
    return getattr(importlib.import_module(module_name), obj_name)


# def get_class(module_name: str, class_name: str) -> type:
#     """dynammically loads the module and returns the class from this file

#     Args:
#         module_name (str): name of python module, (typically a file name without extention)
#         class_name (str): the name of the wanted class

#     Returns:
#         type: The class
#     """
#     return dynamically_load(module_name, class_name)


# def get_function(module_name: str, func_name: str) -> Callable:
#     """dynammically loads the module and returns the function from this file

#     Args:
#         module_name (str): name of python module, (typically a file name without extention)
#         func_name (str): the name of the wanted function

#     Returns:
#         Callable: the function
#     """
#     return dynamically_load(module_name, func_name)


# def get_current_function() -> Callable:
    """return the function that is calling this file

    Returns:
        Callable: function
    """
    return get_caller()


def get_caller_file() -> str:
    """return the name of the file that the caller of the 
    function that's using this function is in

    Returns:
        str: name of file
    """
    frame = inspect.currentframe().f_back.f_back
    return frame.f_code.co_filename


# def get_caller() -> Callable:
    """returns the caller of the function thats using this function

    Returns:
        Callable: caller
    """
    name = get_caller_name(1)
    module = get_caller_file().removesuffix(".py")
    return get_function(module, name)


def get_traceback() -> list[str]:
    """returns the traceback of the stack until current frame

    Returns:
        list[str]: list of frames as strings
    """
    return traceback.format_stack()[8:-2]


class OSType(Enum):
    """enum result for possible results of get_os()
    """
    LINUX = "Linux"
    WINDOWS = "Windows"
    OSX = "OS X"
    UNKNOWN = "Unknown"


def get_os() -> OSType:
    """returns the type of operation system running this code

    Returns:
        OSType: enum result
    """
    p = sys.platform
    if p == "linux" or p == "linux2":
        return OSType.LINUX
    elif p == "darwin":
        return OSType.OSX
    elif p == "win32":
        return OSType.WINDOWS
    return OSType.UNKNOWN


def get_python_version() -> str:
    """returns the python version of the interpreter running this code

    Returns:
        str: version string
    """
    return platform.python_version()


__all__ = [
    "get_caller_name",
    "dynamically_load",
    # "get_class",
    # "get_function",
    # "get_current_function",
    "get_caller_file",
    # "get_caller",
    "get_traceback",
    "OSType",
    "get_os",
    "get_python_version"
]
