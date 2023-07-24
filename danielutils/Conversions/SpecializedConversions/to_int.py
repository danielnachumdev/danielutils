"""functions that convert values to int"""
from typing import Union
import platform
from ..MainConversions import char_to_int
if platform.python_version() >= "3.9":
    from builtins import list as t_list
else:
    from typing import List as t_list


def to_int(value: str) -> Union[int, t_list[int]]:
    """converts a single character or a full string to an int or list of int respectively
    """
    if len(value) == 1:
        return char_to_int(value)
    return [char_to_int(ch) for ch in value]


__all__ = [
    "to_int"
]
