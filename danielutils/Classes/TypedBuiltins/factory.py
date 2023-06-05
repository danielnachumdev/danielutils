from abc import ABC, abstractmethod
from typing import TypeVar, Any, GenericAlias, Generic, Iterable, SupportsIndex, Union, Optional
from danielutils import types_subseteq, isoftype, get_caller_name, overload, get_mro
import types
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


def create_typed_class(name: str, fallback_class: type, bases: Optional[tuple] = None) -> type:
    """will create a base class to inherit from which will enable enforcing runtime type safty
    adds get_params()->tuple which return the supplied type hins from the generic creation of the class

    Args:
        name (str): name of class (can be the same of the derived?)
        fallback_class (type): the fallback class to handle __str__, __repr__ and such. e.g for a typed version of list ('tlist') the fallback class would be 'list'
        bases (tuple, optional): another additional bases that this class should inherit from. Defaults to None.

    Returns:
        type: new class type
    """

    # class InnerMeta(type):
    #     def __new__(mcs, name, bases, namespace):
    #         @classmethod
    #         def __metainstancecheck__(self, other) -> bool:
    #             return __instancecheck__(self, other)
    #         namespace["__instancecheck__"] = __metainstancecheck__
    #         return super().__new__(mcs, name, bases, namespace)

    if bases is None:
        bases = tuple()
    bases_lst: list[type] = [fallback_class]+list(bases)
    for i, base in enumerate(bases_lst):
        bases_lst[i] = base[T]
    del i, base
    cls = types.new_class(name, tuple(bases_lst), {})

    def __class_getitem__(cls, item: type):
        return cls(item)

    def __instancecheck__(self, instance: Any) -> bool:
        if isinstance(instance, cls):
            return types_subseteq(instance.get_params(), self.get_params())
        # type: ignore
        return isoftype(instance, fallback_class[self.get_params()])

    def __init__(self, item) -> None:
        if not get_caller_name(0) == "__class_getitem__":
            raise ValueError(
                f"Can't instantiate {self.__class__.__name__} without a supplied type")
        fallback_class.__init__(self)  # type: ignore
        self._params = (item,) if not isinstance(
            item, Iterable) else tuple(item)

    def subscribable_init(self, *args, **kwargs) -> None:
        raise NotImplementedError(
            "'subscribable_init(self,*args,**kwargs) is an abstract method that must be implemented.")

    def __call__(self, *args, **kwargs):
        # to work with the overloading
        # type(self).subscribable_init(self, *args, **kwargs)
        self.subscribable_init(*args, **kwargs)
        return self

    def __str__(self) -> str:
        res: str = fallback_class.__str__(self)
        if not res.startswith(name):
            return f"{name} {res}"
        return res

    def __repr__(self) -> str:
        res: str = fallback_class.__repr__(self)
        if not res.startswith(name):
            return f"{name} {res}"
        return res

    def get_params(self) -> tuple:
        return self._params

    def __eq__(self, other: Any) -> bool:
        if isoftype(other, cls):
            return self.get_params() == other.get_params()
        return False

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


parent_tlist: type = create_typed_class("tlist", list)
parent_tdict: type = create_typed_class("tdict", dict)
parent_tset: type = create_typed_class("tset", set)
parent_ttuple: type = create_typed_class("ttuple", tuple)


class tlist(parent_tlist, Generic[T]):
    def subscribable_init(self, *args, **kwargs):
        type(self)._additional_init(self, *args, **kwargs)

    @overload
    def _additional_init(self, lst: Union[list, "tlist"]):
        self.extend(lst)

    @_additional_init.overload
    def _init_empty(self) -> None:
        """inits an empty tlist
        """

    @_additional_init.overload
    def _init_from_set_and_dict(self, obj: set | dict):
        """inits the tlist from a set or a dict object
        Args:
            obj (set | dict): the set or dict instance
        """
        self.extend(list(obj))

    def extend(self, other: Iterable) -> None:
        """extends a tlist from a list or a tlist

        Args:
            other (list | tlist): the list to extend from

        Returns:
            tlist: Self
        """
        if isinstance(other, tlist):
            if types_subseteq(other.get_params(), self.get_params()):
                list.extend(self, other)
                return
        for value in other:
            self.append(value)

    def append(self, value: T) -> None:
        """appends a value to the list

        Args:
            value (T): the value to append

        Raises:
            ValueError: if a value is not of the correct type

        Returns:
            tlist: self
        """
        if not isoftype(value, self.get_params()[0]):
            raise TypeError(
                f"In tlist.append: values must be of type {self.get_params()[0]}, but '{value}' is of type {type(value)}")
        list.append(self, value)

    def __add__(self, other: Any) -> "tlist":
        if not isoftype(other, list | tlist):
            raise NotImplementedError()

        # no need to check because the error handling
        # will be done inside extend so the error will
        # propagate up
        res = tlist[self._params](self)  # type:ignore
        res.extend(other)
        return res

    def __mul__(self, other: Any) -> "tlist":
        if not isinstance(other, int):
            raise NotImplementedError()

        res = tlist[self.get_params()[0]](self)  # type:ignore
        for _ in range(other-1):
            res.extend(self)
        return res

    def __setitem__(self, index: SupportsIndex, value: T):  # type:ignore
        if not isoftype(value, self._params):
            raise TypeError(
                "Can't add value to tlist because it is of the wrong type")
        list.__setitem__(self, index, value)


a = tlist[int]([1, 2, 3])
print(a, a.get_params())
print(a[0])
print(a == a)
a.extend(a)
print(a*2)
print(isoftype([1, 2, 3], tlist[int]))
print(isinstance(a, type(a)))


class tdict(parent_tdict, Generic[K, V]):
    def subscribable_init(self, *args, **kwargs):
        print(self.get_params())

    @property
    def _key_t(self):
        return self.get_params()[0]

    @property
    def _value_t(self):
        return self.get_params()[1]

    def __setitem__(self, key: T, value: T):
        if not isoftype(key, self._key_t):
            raise TypeError("")
        if not isoftype(value, self._value_t):
            raise TypeError("")
        dict.__setitem__(self, key, value)


d = tdict[int, int]()
print(d)
d[1] = 1
print(d)
print(isoftype({1: 1}, type(d)))


class tset(parent_tset, Generic[T]):  # type:ignore
    def subscribable_init(self, *args, **kwargs):
        print(self.get_params())


class A:
    pass


class B(A):
    ...


print(get_mro(tlist))
pass

print(b'\x1b[34;41;01m"\x1b[39;49;00m\x1b[34;41;01mHello World\x1b[39;49;00m\x1b[34;41;01m"\x1b[39;49;00m'.decode())
