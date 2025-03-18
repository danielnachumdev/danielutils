import time
from typing import Generic, TypeVar, Optional

from ..aliases import Supplier, Consumer
from .backoff_strategies import ConstantBackOffStrategy

from .backoff_strategy import BackOffStrategy

T = TypeVar("T")


class RetryExecutor(Generic[T]):
    def __init__(self, backoff_strategy: BackOffStrategy = ConstantBackOffStrategy(200)) -> None:
        self._backoff_strategy = backoff_strategy

    def execute(self, supp: Supplier[T], max_retries: int = 5,
                exception_callback: Optional[Consumer[Exception]] = None) -> Optional[T]:

        for i in range(max_retries):

            try:
                return supp()
            except Exception as e:
                if exception_callback:
                    exception_callback(e)

            if i != max_retries - 1:
                self._sleep()
        return None

    def _sleep(self) -> None:
        time.sleep(self._backoff_strategy.get_backoff())


__all__ = [
    "RetryExecutor",
]
