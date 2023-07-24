from typing import Generic, TypeVar
from .factory import create_typed_class
from ...Functions import isoftype
parent: type = create_typed_class("tdict", dict)
K = TypeVar("K")
V = TypeVar("V")


class tdict(parent, Generic[K, V]):
    """like 'dict' but with runtime type safety
    """

    def subscribable_init(self, *args, **kwargs):  # pylint: disable=unused-argument
        """the "real" __init__ function
        """
        print(self.get_params())

    @property
    def _key_t(self):
        return self.get_params()[0]

    @property
    def _value_t(self):
        return self.get_params()[1]

    def __setitem__(self, key: K, value: V):
        if not isoftype(key, self._key_t):
            raise TypeError("")
        if not isoftype(value, self._value_t):
            raise TypeError("")
        dict.__setitem__(self, key, value)


__all__ = [
    "tdict"
]
