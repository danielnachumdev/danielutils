from .Decorators import atomic

# altough it's related to threading, atomic decorator implemented at .Decorators


@atomic
def atomic_print(*args, **kwargs):
    """exactly the same params and behavior as builtin print(), but behaves atomic-ly
    """
    print(*args, **kwargs)


__all__ = [
    "atomic_print"
]
