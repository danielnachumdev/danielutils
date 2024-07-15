from ..backoff_strategy import BackOffStrategy


class ConstantBackOffStrategy(BackOffStrategy):
    """
    will always back off exactly the same amount of time

    :param delay: The amount of milliseconds to sleep
    """

    def __init__(self, delay: int) -> None:
        if not delay >= 0:
            raise ValueError("delay must be positive")
        super().__init__(lambda: delay)


__all__ = [
    "ConstantBackOffStrategy"
]
