import sys
import platform
from enum import Enum


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
    if p in {"linux", "linux2"}:
        return OSType.LINUX
    if p == "darwin":
        return OSType.OSX
    if p == "win32":
        return OSType.WINDOWS
    return OSType.UNKNOWN


def _get_python_version_untyped() -> tuple:
    values = (int(v) for v in platform.python_version().split("."))
    return tuple(values)  # type:ignore


if _get_python_version_untyped() < (3, 9):
    from typing import Tuple as t_tuple
else:
    from builtins import tuple as t_tuple  # type:ignore


def get_python_version() -> t_tuple[int, int, int]:
    """return the version of python that is currently running this code

    Returns:
        tuple[int, int, int]: version
    """
    return _get_python_version_untyped()  # type:ignore


__all__ = [
    "OSType",
    "get_os",
    "get_python_version"
]
