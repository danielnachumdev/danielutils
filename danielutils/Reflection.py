import inspect
import traceback
import platform
import sys
from enum import Enum


def get_caller_name() -> str:
    """returns the name caller of the function

    Returns:
        str: name of caller
    """
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

    return inspect.currentframe().f_back.f_back.f_code.co_name


def get_traceback() -> list[str]:
    return traceback.format_stack()[8:-2]


class OSType(Enum):
    LINUX = "Linux"
    WINDOWS = "Windows"
    OSX = "OS X"
    UNKNOWN = "Unknown"


def get_os() -> OSType:
    p = sys.platform
    if p == "linux" or p == "linux2":
        return OSType.LINUX
    elif p == "darwin":
        return OSType.OSX
    elif p == "win32":
        return OSType.WINDOWS
    return OSType.UNKNOWN


def get_python_version():
    return platform.python_version()


__all__ = [
    "get_caller_name",
    "get_traceback",
    "OSType",
    "get_os",
    "get_python_version"
]
