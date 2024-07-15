from danielutils import Supplier


class BackOffStrategy:
    """
    A class to create a common abstraction for backoff strategies
    """

    def __init__(self, supp: Supplier[int]) -> None:
        self._supp = supp

    def get_backoff(self) -> int:
        """

        :return: amount of milliseconds to sleep
        """
        return self._supp()


__all__ = [
    "BackOffStrategy"
]
