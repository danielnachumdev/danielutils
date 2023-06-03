from typing import Any


class property2:
    def __init__(self, func):
        self.gfunc = func
        self.sfunc = None
        self.dfunc = None

    def setter(self, func):
        self.sfunc = func
        return self

    def deleter(self, func):
        self.dfunc = func
        return self

    def __get__(self, instance: Any, owner: type | None = None) -> Any:
        if callable(self.gfunc):
            return self.gfunc(instance)
        raise ValueError("Can't use unset getter function")

    def __set__(self,  instance: Any, value: Any) -> None:
        if callable(self.sfunc):
            return self.sfunc(instance)
        raise ValueError("Can't use unset getter function")

    def __delete__(self, instance: Any) -> None:
        if callable(self.dfunc):
            return self.dfunc(instance)
        raise ValueError("Can't use unset getter function")


__all__ = [
    "property2"
]
