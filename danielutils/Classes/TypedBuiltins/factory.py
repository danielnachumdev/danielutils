import types
from abc import abstractmethod
from typing import Any, Iterable
from ...Functions.types_subseteq import types_subseteq
from ...Functions.isoftype import isoftype
from ...Reflection.Function import get_caller_name


def create_typed_class(name: str, fallback_class: type = object) -> type:
    """will create a base class to inherit from which will enable enforcing runtime type safety.

    ### The following functions are added for use:

    * get_params()->tuple which return the supplied type hins from the generic creation of the class
    * subscribable_init(self,*args,**kwargs) which is the new "__init__"
    * on_call(self,*args,**kwargs) which is the new "__call__"

    Args:
        name (str): name of class (can be the same of the derived?)
        fallback_class (type): the fallback class to handle __str__, __repr__ and such. e.g for a typed version of list ('tlist') the fallback class would be 'list'
        bases (tuple, optional): another additional bases that this class should inherit from. Defaults to None.

    Returns:
        type: new class type
    """
    cls = types.new_class(name, (fallback_class,), dict())

    def __class_getitem__(cls, item: type):
        return cls(item)

    def __instancecheck__(self, instance: Any) -> bool:
        if isinstance(instance, cls):

            return types_subseteq(
                instance.get_params(),  # type:ignore
                self.get_params()
            )

        return isoftype(
            instance,
            fallback_class[self.get_params()]  # type:ignore
        )

    def __init__(self, item) -> None:
        if not get_caller_name(0) == "__class_getitem__":
            raise ValueError(
                f"Can't instantiate {self.__class__.__name__} without a supplied type")
        fallback_class.__init__(self)  # type: ignore
        # pylint: disable=protected-access
        self._params = (item,) if not isinstance(
            item, Iterable) else tuple(item)
        self._inited = False

    def subscribable_init(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "'subscribable_init(self,*args,**kwargs) is an abstract method that must be implemented.")

    def on_call(self, *args, **kwargs) -> Any:
        raise NotImplementedError(
            "'on_call(self,*args,**kwargs) is an abstract method that must be implemented.")

    def __call__(self, *args, **kwargs):
        # pylint: disable=protected-access
        if not self._inited:
            self_inited = True
            # to work with overloading
            type(self).subscribable_init(self, *args, **kwargs)
            # self.subscribable_init(*args, **kwargs)
            return self
        return self.on_call(self, *args, **kwargs)

    def __str__(self) -> str:
        res: str = fallback_class.__str__(self)  # type:ignore
        if not res.startswith(name):
            return f"{name} {res}"
        return res

    def __repr__(self) -> str:
        res: str = fallback_class.__repr__(self)  # type:ignore
        if not res.startswith(name):
            return f"{name} {res}"
        return res

    def get_params(self) -> tuple:
        # pylint: disable=protected-access
        return self._params

    def __eq__(self, other: Any) -> bool:
        if isoftype(other, cls):
            return self.get_params() == other.get_params()
        return False

    # pylint: disable=unused-argument
    def __init_subclass__(subcls, **kwargs):
        if hasattr(subcls, "__init__"):
            curr_init = getattr(subcls, "__init__")
            if curr_init is not __init__:
                raise ValueError(
                    "Can't override '__init__', use 'subscribable_init(self,*args,**kwargs)' instead.")

    for func, decorator in [
        (__class_getitem__, classmethod),
        (__instancecheck__, None),
        (subscribable_init, abstractmethod),
        (__init__, None),
        (__call__, None),
        (__str__, None),
        (__repr__, None),
        (__eq__, None),
        (get_params, None),
        (__init_subclass__, classmethod)
    ]:
        if decorator is not None:
            func = decorator(func)  # type:ignore
        setattr(cls, func.__name__, func)

    return cls


__all__ = [
    "create_typed_class"
]
