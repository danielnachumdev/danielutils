import logging
from ..aliases import Supplier
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class BackOffStrategy:
    """
    A class to create a common abstraction for backoff strategies
    """

    def __init__(self, supp: Supplier[float]) -> None:
        self._supp = supp

    def get_backoff(self) -> float:
        """
        Get the backoff time in milliseconds.

        :return: amount of milliseconds to sleep
        """
        backoff_time = self._supp()
        return backoff_time


__all__ = [
    "BackOffStrategy"
]
