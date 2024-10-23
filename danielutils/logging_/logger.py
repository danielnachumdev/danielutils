import json
from datetime import datetime
from typing import Type, Optional, Dict, List

from .log_level import LogLevel
from .logger_strategy_impl_base import LoggerStrategyImplBase


class _LoggerImpl:
    def __init__(self, origin: Type):
        self.origin = origin

    @classmethod
    def parse_message(
            cls,
            origin: Type,
            logger_id: Optional,
            channel: str,
            level: LogLevel,
            message: str,
            module: Optional[str] = None,
            cls_name: Optional[str] = None,
            metadata: Optional[Dict] = None
    ) -> str:
        d = dict(
            timestamp=str(datetime.now()),
            origin=origin.__qualname__,
            logger_id=logger_id,
            channel=channel,
            level=level.name,
            message=message
        )
        if module:
            d.update({'module': module})

        if cls_name:
            d.update({'cls': cls_name})

        if metadata:
            d.update({'metadata': metadata})
        s = json.dumps(d)
        return f"{s}\n"

    def _log(self, level: LogLevel, message: str, channel: str, **metadata):
        message = str(message)
        for logger in LoggerStrategyImplBase._loggers[channel]:
            logger(self.parse_message(
                self.origin,
                logger.logger_id,
                channel,
                level,
                message,
                metadata.get("cls", {}).get("__module__", None),
                metadata.pop("cls", {}).get("__qualname__", None),
                metadata
            ))

    def debug(self, message: str, channel: str = "all", **metadata):
        self._log(LogLevel.DEBUG, message, channel, **metadata)

    def info(self, message: str, channel: str = "all", **metadata):
        self._log(LogLevel.INFO, message, channel, **metadata)

    def warning(self, message: str, channel: str = "all", **metadata):
        self._log(LogLevel.WARNING, message, channel, **metadata)

    def error(self, message: str, channel: str = "all", **metadata):
        self._log(LogLevel.ERROR, message, channel, **metadata)


class Logger:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls._logger = _LoggerImpl(cls)
        cls._registered_loggers: List[LoggerStrategyImplBase] = []
        cls.init_subscribers()

    @classmethod
    @property
    def logger(cls) -> _LoggerImpl:
        return cls._logger

    @classmethod
    def init_subscribers(cls):
        pass

    @classmethod
    def register_logger(cls, logger: LoggerStrategyImplBase) -> None:
        cls._registered_loggers.append(logger)


class GlobalLogger(Logger):
    pass


__all__ = [
    "Logger",
    "GlobalLogger"
]
