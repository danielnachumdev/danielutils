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


__all__ = [
    "OSType",
    "get_os",
]
