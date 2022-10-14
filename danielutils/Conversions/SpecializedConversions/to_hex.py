from ...Decorators import overload
from ..MainConversions import *


@overload(int)
def to_hex(v: int) -> str:
    # docstring at last implementation
    return int_to_hex(v)


@overload(str)
def to_hex(v: str) -> str:
    """to_hex has several options:\n
    1. type(v) == int\n
    2. type(v) == str and len(v) == 1

    Returns:
        str: str of the hex value
    """
    return char_to_hex(v)


__all__ = [
    "to_hex"
]
