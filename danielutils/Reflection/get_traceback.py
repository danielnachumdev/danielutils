import traceback
import platform
if platform.python_version() < "3.9":
    from typing import List as t_list
else:
    from builtins import list as t_list


def get_traceback() -> t_list[str]:
    """returns the traceback of the stack until current frame

    Returns:
        list[str]: list of frames as strings
    """
    return traceback.format_stack()[8:-2]


__all__ = [
    "get_traceback"
]
