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
        return self.gfunc(instance)

    def __set__(self,  instance: Any, value: Any) -> None:
        return self.sfunc(instance, value)

    def __delete__(self, instance: Any) -> None:
        return self.dfunc(instance)


__all__ = [
    "property2"
]
