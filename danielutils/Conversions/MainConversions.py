from ..Decorators import validate, overload


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


@validate(bytes)
def bytes_to_str(b: bytes) -> str:
    return b.decode("utf-8")


@validate(str)
def str_to_bytes(s: str) -> bytes:
    return bytes(s, encoding='utf-8')


__all__ = [
    "char_to_int",
    "int_to_char",
    "hex_to_char",
    "hex_to_dec",
    "char_to_hex",
    "dec_to_hex",
    "int_to_hex",
    "bytes_to_str",
    "str_to_bytes"
]
