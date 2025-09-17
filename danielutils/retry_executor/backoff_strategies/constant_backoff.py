import logging
from ..backoff_strategy import BackOffStrategy
from ...logging_.utils import get_logger

logger = get_logger(__name__)


class ConstantBackOffStrategy(BackOffStrategy):
    """
    will always back off exactly the same amount of time

    :param delay: The amount of milliseconds to sleep
    """

    def __init__(self, delay: float) -> None:
        if not delay >= 0:
            logger.error(f"Invalid delay value: {delay} - must be positive")
            raise ValueError("delay must be positive")
        delay = float(delay)
        super().__init__(lambda: delay)


__all__ = [
    "ConstantBackOffStrategy"
]
