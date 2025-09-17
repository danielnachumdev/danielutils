import logging
from collections import defaultdict
from typing import Dict, List, Callable
from ..utils import get_logger

logger = get_logger(__name__)


class LoggerStrategyImplBase:
    _loggers: Dict[str, List['LoggerStrategyImplBase']] = defaultdict(list)

    def __init__(self, output_func: Callable[[str], None], logger_id: str, channel: str = "all"):
        logger.info("Initializing LoggerStrategyImplBase: id=%s, channel=%s", logger_id, channel)
        self.output_func: Callable[[str], None] = output_func
        self.channel: str = channel
        self.logger_id: str = logger_id
        LoggerStrategyImplBase._loggers[channel].append(self)
        logger.info("Logger %s added to channel %s, total loggers: %s", logger_id, channel, len(LoggerStrategyImplBase._loggers[channel]))

    def __call__(self, s: str) -> None:
        self.output_func(s)

    def delete(self) -> None:
        logger.info("Deleting logger %s from channel %s", self.logger_id, self.channel)
        LoggerStrategyImplBase._loggers[self.channel].remove(self)
        logger.info("Logger deleted, remaining loggers in channel: %s", len(LoggerStrategyImplBase._loggers[self.channel]))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()


__all__ = [
    "LoggerStrategyImplBase"
]
