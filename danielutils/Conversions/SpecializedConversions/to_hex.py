from ...MetaClasses.OverloadMeta import OverloadMeta
from ..MainConversions import int_to_hex, char_to_hex


@OverloadMeta.overload
def to_hex(v: int) -> str:
    # docstring at last implementation
    return int_to_hex(v)


@to_hex.overload
def to_hex2(v: str) -> str:
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
