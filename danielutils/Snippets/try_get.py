from typing import Callable, Any, Optional


def try_get(supplier: Callable[[], Any]) -> Optional[Any]:
    try:
        return supplier()
    except:
        return None


__all__ = [
    "try_get"
]
