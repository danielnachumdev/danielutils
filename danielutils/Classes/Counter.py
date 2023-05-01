class Counter:
    """A simple counter class
    """

    def __init__(self, initial_value: int | float = 0, increment_amount: int | float = 1):
        self.value = initial_value
        self.increment_value = increment_amount

    def increment(self):
        """increments the stored value by the increment amount
        """
        self.value += self.increment_value

    def decrement(self):
        """decrements the stored value by the increment amount
        """
        self.value -= self.increment_value

    def get(self) -> int | float:
        """returns the current value of the counter

        Returns:
            int | float: value
        """
        return self.value

    def set(self, value: int | float):
        """sets the values of the counter

        Args:
            value (int | float): value to set
        """
        self.value = value


__all__ = [
    "Counter"
]
