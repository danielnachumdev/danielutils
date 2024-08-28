from ..backoff_strategy import BackOffStrategy


class ExponentialBackOffStrategy(BackOffStrategy):
    def __init__(self, initial: float) -> None:
        if not initial >= 0:
            raise ValueError("initial must be positive")
        attempt: int = 1

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            return initial ** (attempt - 1)

        super().__init__(inner)


__all__ = [
    "ExponentialBackOffStrategy"
]
