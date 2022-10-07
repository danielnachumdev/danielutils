from .Decorators import validate, overload
from typing import Any


@validate([str, lambda s:len(s) == 1, "len(s) must be 1"])
def char_to_int(c: str) -> int:
    """convert char to its representing int value

    Args:
        c (str): char to ceonvert

    Returns:
        int: int value
    """
    return ord(c)


@validate(int)
def int_to_char(num: int) -> str:
    """convert int to its correspondint char

    Args:
        num (int): number to convert

    Returns:
        str: result charachter
    """
    return chr(num)


@validate(str)
def hex_to_char(h: str) -> str:
    """convert hex number to char

    Args:
        h (str): number to convert

    Returns:
        str: result char
    """
    return int_to_char(hex_to_dec(h))


@validate(str)
def hex_to_dec(h: str) -> int:
    """convert hex to dec

    Args:
        h (str): converts base 16 to base 10

    Returns:
        int: decimal value for hex number
    """
    return int(h, 16)


@validate([str, lambda s:len(s) == 1, "len(s) must be 1"])
def char_to_hex(c: str) -> str:
    """convert char to hex

    Args:
        c (str): char to convert

    Returns:
        str: hex representation
    """
    return int_to_hex(char_to_int(c))


@validate(int)
def dec_to_hex(num: int) -> str:
    """conver decimal number to hex

    Args:
        num (int): number to convert

    Returns:
        str: _description_
    """
    return int_to_hex(num)


@validate(int)
def int_to_hex(num: int) -> str:
    return hex(num)


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
    "char_to_int",
    "int_to_char",
    "hex_to_char",
    "hex_to_dec",
    "char_to_hex",
    "dec_to_hex",
    "int_to_hex",
    "to_hex"
]
