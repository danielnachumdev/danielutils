from collections import defaultdict
from typing import Dict, List, Callable


class LoggerStrategyImplBase:
    _loggers: Dict[str, List['LoggerStrategyImplBase']] = defaultdict(list)

    def __init__(self, output_func: Callable[[str], None], logger_id: str, channel: str = "all"):
        self.output_func: Callable[[str], None] = output_func
        self.channel: str = channel
        self.logger_id: str = logger_id
        LoggerStrategyImplBase._loggers[channel].append(self)

    def __call__(self, s: str) -> None:
        self.output_func(s)

    def delete(self) -> None:
        LoggerStrategyImplBase._loggers[self.channel].remove(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()


__all__ = [
    "LoggerStrategyImplBase"
]
