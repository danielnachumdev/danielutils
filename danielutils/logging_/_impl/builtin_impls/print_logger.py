import logging
from ...utils import get_logger
from ..logger_strategy_impl_base import LoggerStrategyImplBase

logger = get_logger(__name__)


class PrintLogger(LoggerStrategyImplBase):
    def __init__(self, logger_id: str, channel: str = "all"):
        logger.info(f"Initializing PrintLogger: id={logger_id}, channel={channel}")
        
        def print_func(s: str):
            print(s, end="")
        
        super().__init__(print_func, logger_id, channel)
        logger.info(f"PrintLogger {logger_id} initialized successfully")


__all__ = [
    "PrintLogger"
]
