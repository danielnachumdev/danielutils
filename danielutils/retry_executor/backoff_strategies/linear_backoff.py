from ..backoff_strategy import BackOffStrategy


class LinerBackoffStrategy(BackOffStrategy):
    def __init__(self, initial: float, additive_term: float) -> None:
        attempt = 1

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            return initial + additive_term * (attempt - 1)

        super().__init__(inner)


__all__ = [
    'LinerBackoffStrategy'
]
