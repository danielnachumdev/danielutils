import json
import logging
from datetime import datetime
from typing import Any, Type, Optional, Dict, List

from .log_level import LogLevel
from .logger_strategy_impl_base import LoggerStrategyImplBase
from ..utils import get_logger

logger = get_logger(__name__)


class _LoggerImpl:
    def __init__(self, origin: Type):
        self.origin = origin

    @classmethod
    def parse_message(
            cls,
            origin: Type,
            logger_id: Optional[str],
            channel: str,
            level: LogLevel,
            message: str,
            module: Optional[str] = None,
            cls_name: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None
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
        loggers_count = len(LoggerStrategyImplBase._loggers[channel])
        
        for logger_instance in LoggerStrategyImplBase._loggers[channel]:
            logger_instance(self.parse_message(
                self.origin,
                logger_instance.logger_id,
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
    def __init_subclass__(cls, **kwargs) -> None:
        logger.info("Initializing Logger subclass: %s", cls.__qualname__)
        cls._logger = _LoggerImpl(cls)
        cls._registered_loggers: List[LoggerStrategyImplBase] = []
        cls.init_subscribers()
        logger.info("Logger subclass %s initialized successfully", cls.__qualname__)

    @classmethod
    @property
    def logger(cls) -> _LoggerImpl:
        return cls._logger

    @classmethod
    def init_subscribers(cls):
        pass

    @classmethod
    def register_logger(cls, logger_instance: LoggerStrategyImplBase) -> None:
        logger.info("Registering logger %s for class %s", logger_instance.logger_id, cls.__qualname__)
        cls._registered_loggers.append(logger_instance)
        logger.info("Logger registered successfully, total registered: %s", len(cls._registered_loggers))


class GlobalLogger(Logger):
    pass


__all__ = [
    "Logger",
    "GlobalLogger"
]
