from typing import Callable

from ..backoff_strategy import BackOffStrategy


class FunctionalBackoffStrategy(BackOffStrategy):
    def __init__(self, func: Callable[[int], float]) -> None:
        attempt = 1

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            return func(attempt - 1)

        super().__init__(inner)


__all__ = [
    "FunctionalBackoffStrategy"
]
