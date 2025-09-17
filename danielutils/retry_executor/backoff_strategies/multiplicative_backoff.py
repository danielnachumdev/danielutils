import logging
from ..backoff_strategy import BackOffStrategy
from ...logging_.utils import get_logger

logger = get_logger(__name__)


class MultiplicativeBackoff(BackOffStrategy):
    def __init__(self, initial_backoff: float) -> None:
        attempt = 1

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            backoff_time = initial_backoff * (attempt - 1)
            return backoff_time

        super().__init__(inner)


__all__ = [
    'MultiplicativeBackoff'
]
