from typing import Union
from ..metaclasses import AtomicClassMeta


class Counter:
    """A simple counter class
    """

    def __init__(self, initial_value: Union[int, float] = 0, increment_amount: Union[int, float] = 1) -> None:
        self.value = initial_value
        self.increment_value = increment_amount

    def increment(self) -> None:
        """increments the stored value by the increment amount
        """
        self.value += self.increment_value

    def decrement(self) -> None:
        """decrements the stored value by the increment amount
        """
        self.value -= self.increment_value

    def get(self) -> Union[int, float]:
        """returns the current value of the counter

        Returns:
            Union[int, float]: value
        """
        return self.value

    def set(self, value: Union[int, float]):
        """sets the values of the counter

        Args:
            value (Union[int, float]): value to set
        """
        self.value = value


class AtomicCounter(Counter, metaclass=AtomicClassMeta):  # type:ignore
    """A Counter Class which is Atomic
    """


__all__ = [
    "Counter",
    "AtomicCounter"
]
