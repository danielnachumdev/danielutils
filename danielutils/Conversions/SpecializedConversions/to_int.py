from ...Decorators import overload
from ..MainConversions import *
from typing import Union


def to_int(value: str) -> Union[int, list[int]]:
    """converts a single character or a full string to an int or list of int respectively
    """
    if len(value) == 1:
        return char_to_int(value)
    return [char_to_int(ch) for ch in value]


__all__ = [
    "to_int"
]
