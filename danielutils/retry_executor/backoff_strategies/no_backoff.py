import logging
from ..backoff_strategy import BackOffStrategy
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class NoBackOffStrategy(BackOffStrategy):

    def __init__(self) -> None:
        logger.debug("Initializing NoBackOffStrategy (no delay)")
        super().__init__(lambda: 0.0)


__all__ = [
    'NoBackOffStrategy',
]
