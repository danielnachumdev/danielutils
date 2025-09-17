import logging
from ..backoff_strategy import BackOffStrategy
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class LinerBackoffStrategy(BackOffStrategy):
    def __init__(self, initial: float, additive_term: float) -> None:
        attempt = 1

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            backoff_time = initial + additive_term * (attempt - 1)
            return backoff_time

        super().__init__(inner)


__all__ = [
    'LinerBackoffStrategy'
]
