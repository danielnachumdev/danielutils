from __future__ import annotations
from typing import Iterable
# from .tbase import tbase
from ...Decorators import overload
from ...Functions import isoftype


class tdict(dict):
    """like builtin dict but only a specif type is allowed
    """
    @overload(None, type, type)
    def __init__(self, key_t: type, val_t: type):
        self.key_t: type = key_t
        self.val_t: type = val_t
        super().__init__()

    @overload(None, type, type, Iterable)
    def __init__(self, key_t: type, val_t: type, iterable: Iterable[tuple]):
        self.key_t: type = key_t
        self.val_t: type = val_t
        super().__init__(iterable)

    @overload(None, type, type, dict)
    def __init__(self, key_t: type, val_t: type, ** kwargs):
        """dict(type,type) -> new empty dictionary dict(mapping) -> new dictionary initialized from a mapping object's
                (key, value) pairs
            dict(type,type,iterable) -> new dictionary initialized as if via:
                d = {} for k, v in iterable:
                    d[k] = v
            dict(type,type,**kwargs) -> new dictionary initialized with the name=value pairs
                in the keyword argument list. For example: dict(one=1, two=2)
        """
        super().__init__(**kwargs)
        self.key_t: type = key_t
        self.val_t: type = val_t

    def __setitem__(self, key, value) -> None:
        if not isoftype(key, self.key_t):
            raise TypeError(
                f"In class 'tdict' error creating new key-value pair as"
                f" key = '{key}' is not of type '{self.key_t}'")
        if not isoftype(value, self.val_t):
            raise TypeError(
                f"In class 'tdict' error creating new key-value pair"
                f" as value = '{value}' is not of type '{ self.val_t}'")
        super().__setitem__(key, value)

    def __str__(self):
        return f"dict[{self.key_t.__name__}, {self.val_t.__name__}]: {super().__str__()}"


__all__ = [
    "tdict"
]
