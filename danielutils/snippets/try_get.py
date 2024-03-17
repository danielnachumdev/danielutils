from typing import Callable, Any, Optional


def try_get(supplier: Callable[[], Any]) -> Optional[Any]:
    """try to get a value from a function and return the value or return None on fail

    Args:
        supplier (Callable[[], Any]): supplier function

    Returns:
        Optional[Any]: return value
    """
    try:
        return supplier()
    except:
        return None


__all__ = [
    "try_get"
]
