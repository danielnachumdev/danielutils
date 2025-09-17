import logging
from typing import Callable

from ..backoff_strategy import BackOffStrategy
from ...logging_.utils import get_logger

logger = get_logger(__name__)


class FunctionalBackoffStrategy(BackOffStrategy):
    def __init__(self, func: Callable[[int], float]) -> None:
        logger.debug(f"Initializing FunctionalBackoffStrategy with function: {func.__name__ if hasattr(func, '__name__') else type(func).__name__}")
        attempt = 1
        logger.debug("Setting up functional backoff with custom function")

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            backoff_time = func(attempt - 1)
            logger.debug(f"Functional backoff attempt {attempt}: {backoff_time}ms (func({attempt - 1}))")
            return backoff_time

        super().__init__(inner)
        logger.debug("FunctionalBackoffStrategy initialized successfully")


__all__ = [
    "FunctionalBackoffStrategy"
]
