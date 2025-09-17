import logging
import time
from typing import Generic, TypeVar, Optional

from ..aliases import Supplier, Consumer
from .backoff_strategies import ConstantBackOffStrategy

from .backoff_strategy import BackOffStrategy
from .logging_.utils import get_logger

T = TypeVar("T")

logger = get_logger(__name__)


class RetryExecutor(Generic[T]):
    def __init__(self, backoff_strategy: BackOffStrategy = ConstantBackOffStrategy(200)) -> None:
        self._backoff_strategy = backoff_strategy
        logger.info(f"RetryExecutor initialized with backoff strategy: {type(backoff_strategy).__name__}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning(f"RetryExecutor context exited with exception: {exc_type.__name__}: {exc_val}")

    def execute(self, supp: Supplier[T], max_retries: int = 5,
                exception_callback: Optional[Consumer[Exception]] = None) -> Optional[T]:
        logger.info(f"Starting retry execution with max_retries={max_retries}")
        
        for i in range(max_retries):
            try:
                result = supp()
                logger.info(f"Execution succeeded on attempt {i + 1}")
                return result
            except Exception as e:
                logger.warning(f"Attempt {i + 1} failed with {type(e).__name__}: {e}")
                if exception_callback:
                    exception_callback(e)

            if i != max_retries - 1:
                self._sleep()
        
        logger.error(f"All {max_retries} attempts failed")
        return None

    def _sleep(self) -> None:
        backoff_time = self._backoff_strategy.get_backoff() / 1000
        time.sleep(backoff_time)


__all__ = [
    "RetryExecutor",
]
