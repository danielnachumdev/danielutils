from typing import Callable
from ..Decorators import atomic


class AtomicClassMeta(type):
    """will make all of the class's function atomic
    """
    def __new__(mcs, name, bases, namespace):
        for k, v in namespace.items():
            if isinstance(v, Callable):
                namespace[k] = atomic(v)
        for base in bases:
            for k, v in base.__dict__.items():
                if isinstance(v, Callable):
                    if k not in namespace:
                        namespace[k] = atomic(v)
                    # else:
                    #     breakpoint()
                    #     pass
        return super().__new__(mcs, name, bases, namespace)


__all__ = [
    "AtomicClassMeta"
]
