from ..backoff_strategy import BackOffStrategy


class NoBackOffStrategy(BackOffStrategy):

    def __init__(self) -> None:
        super().__init__(lambda: 0)


__all__ = [
    'NoBackOffStrategy',
]
