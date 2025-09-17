import logging
from ..backoff_strategy import BackOffStrategy
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class ExponentialBackOffStrategy(BackOffStrategy):
    def __init__(self, initial: float) -> None:
        if not initial >= 0:
            logger.error(f"Invalid initial value: {initial} - must be positive")
            raise ValueError("initial must be positive")
        attempt: int = 1

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            backoff_time = initial ** (attempt - 1)
            return backoff_time

        super().__init__(inner)


__all__ = [
    "ExponentialBackOffStrategy"
]
