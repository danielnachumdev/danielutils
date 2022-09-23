from .Decorators import validate, overload
from typing import Any


@validate([str, lambda s:len(s) == 1, "len(s) must be 1"])
def char_to_int(c: str) -> int:
    return ord(c)


@validate(int)
def int_to_char(num: int) -> str:
    return chr(num)


@validate(str)
def hex_to_char(h: str) -> str:
    return int_to_char(hex_to_dec(h))


@validate(str)
def hex_to_dec(h: str) -> int:
    return int(h, 16)


@validate([str, lambda s:len(s) == 1, "len(s) must be 1"])
def char_to_hex(c: str) -> str:
    return int_to_hex(char_to_int(c))


@validate(int)
def dec_to_hex(num: int) -> str:
    return int_to_hex(num)


@validate(int)
def int_to_hex(num: int) -> str:
    return hex(num)


@overload(int)
def to_hex(v: int) -> str:
    # docstring at last implementation
    return int_to_hex(v)


@overload(str)
def to_hex(v: Any) -> str:
    """to_hex has several options:\n
    1. type(v) == int\n
    2. type(v) == str and len(v) == 1

    Returns:
        str: str of the hex value
    """
    return char_to_hex(v)
