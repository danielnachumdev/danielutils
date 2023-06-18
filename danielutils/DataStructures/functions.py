from typing import Any
from ..Functions import isoftype


def default_weight_function(v: Any) -> int | float:
    """will return the weight of an object

    Args:
        v (Any): object

    Raises:
        AttributeError: if the object is not a number or doesn't have __weight__ function defined

    Returns:
        int | float: the object's weight
    """
    if isoftype(v, int | float):
        return v
    if hasattr(v, "__weight__"):
        return v.__weight__()
    raise AttributeError(f"{v} has no __weight__ function")


__all__ = [
    "default_weight_function"
]
