from typing import Union
from ..Decorators import validate


@validate
def sign(v: Union[int, float]) -> int:
    """return the sign of the number

    Args:
        v (Union[int, float]): number

    Returns:
        int: either 1 or -1
    """
    if v >= 0:
        return 1
    return -1


__all__ = [
    "sign"
]
