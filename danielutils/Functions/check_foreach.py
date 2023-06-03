from typing import Sequence, Any, Callable


def check_foreach(values: Sequence[Any], condition: Callable[[Any], bool]) -> bool:
    """

    Args:
        values (Sequence[Any]): Values to perform check on
        condition (Callable[[Any], bool]): Condition to check on all values

    Returns:
        bool: returns True iff condition return True for all values individually
    """
    if not isinstance(values, Sequence):
        pass
    if not callable(condition):
        pass
    for v in values:
        if not condition(v):
            return False
    return True


__all__ = [
    "check_foreach"
]
