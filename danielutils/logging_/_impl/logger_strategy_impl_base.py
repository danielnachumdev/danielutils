import logging
from collections import defaultdict
from typing import Dict, List, Callable
from ..utils import get_logger

logger = get_logger(__name__)


class LoggerStrategyImplBase:
    _loggers: Dict[str, List['LoggerStrategyImplBase']] = defaultdict(list)

    def __init__(self, output_func: Callable[[str], None], logger_id: str, channel: str = "all"):
        logger.info(f"Initializing LoggerStrategyImplBase: id={logger_id}, channel={channel}")
        self.output_func: Callable[[str], None] = output_func
        self.channel: str = channel
        self.logger_id: str = logger_id
        LoggerStrategyImplBase._loggers[channel].append(self)
        logger.info(f"Logger {logger_id} added to channel {channel}, total loggers: {len(LoggerStrategyImplBase._loggers[channel])}")

    def __call__(self, s: str) -> None:
        self.output_func(s)

    def delete(self) -> None:
        logger.info(f"Deleting logger {self.logger_id} from channel {self.channel}")
        LoggerStrategyImplBase._loggers[self.channel].remove(self)
        logger.info(f"Logger deleted, remaining loggers in channel: {len(LoggerStrategyImplBase._loggers[self.channel])}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()


__all__ = [
    "LoggerStrategyImplBase"
]
