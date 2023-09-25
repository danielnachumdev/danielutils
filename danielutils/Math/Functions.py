from typing import Union
from ..decorators import validate


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


def lp_norm(arr, p: Union[int, float]) -> float:
    """calculates a norm over the data
    """
    return root(sum(abs(v)**p for v in arr), p)


def root(value, power: Union[int, float]) -> float:
    """calculates any root over value
    """
    return value**(1/power)


__all__ = [
    "sign"
]
