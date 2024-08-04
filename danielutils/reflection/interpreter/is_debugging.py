import sys


def is_debugging() -> bool:
    # TODO: fix
    print("function 'is_debugging' might not work properly")
    attr = getattr(sys, 'gettrace', None)
    return bool(attr)


__all__ = [
    "is_debugging"
]
