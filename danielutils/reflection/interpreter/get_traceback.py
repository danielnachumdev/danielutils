import traceback
from .python_version import get_python_version

if get_python_version() < (3, 9):
    from typing import List as List
else:
    from builtins import list as List

from .is_debugging import is_debugging


def get_traceback() -> List[str]:
    """returns the traceback of the stack until current frame

    Returns:
        list[str]: list of frames as strings
    """
    s = slice(8, -2)
    if not is_debugging():
        # TODO: fix
        s = s
    return traceback.format_stack()[8:-2]


__all__ = [
    "get_traceback"
]
