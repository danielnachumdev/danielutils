from ..backoff_strategy import BackOffStrategy


class MultiplicativeBackoff(BackOffStrategy):
    def __init__(self, initial_backoff: float) -> None:
        attempt = 1

        def inner() -> float:
            nonlocal attempt
            attempt += 1
            return initial_backoff * (attempt - 1)

        super().__init__(inner)


__all__ = [
    'MultiplicativeBackoff'
]
