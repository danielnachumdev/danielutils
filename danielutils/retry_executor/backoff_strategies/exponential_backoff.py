from ..backoff_strategy import BackOffStrategy


class ExponentialBackOffStrategy(BackOffStrategy):
    def __init__(self, initial: int, multiplier: float) -> None:
        if not initial >= 0:
            raise ValueError("initial must be positive")
        if not multiplier >= 0:
            raise ValueError("multiplier must be positive")
        prev: float = 1.0

        def inner() -> int:
            nonlocal prev
            return initial ** (prev := prev * multiplier)

        super().__init__(inner)


__all__ = [
    "ExponentialBackOffStrategy"
]
