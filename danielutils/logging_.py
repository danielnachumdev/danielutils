import json
from collections import defaultdict
from datetime import datetime
from enum import IntEnum
from pathlib import Path
from typing import Optional, Dict, List, Callable, Type

from danielutils import delete_file


class LogLevel(IntEnum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3


class LoggerOutput:
    _loggers: Dict[str, List['LoggerOutput']] = defaultdict(list)

    def __init__(self, output_func: Callable[[str], None], logger_id: str, channel: str = "all"):
        self.output_func: Callable[[str], None] = output_func
        self.channel: str = channel
        self.logger_id: str = logger_id
        LoggerOutput._loggers[channel].append(self)

    def __call__(self, s: str) -> None:
        self.output_func(s)

    def delete(self) -> None:
        LoggerOutput._loggers[self.channel].remove(self)


class PrintLoggerOutput(LoggerOutput):
    def __init__(self, logger_id: str, channel: str = "all"):
        super().__init__(lambda s: print(s, end=""), logger_id, channel)


class FIleLoggerOutput(LoggerOutput):
    def __init__(self, output_path: str, logger_id: str, delete_if_already_exists: bool = True, channel: str = "all"):
        if delete_if_already_exists:
            delete_file(output_path)
        self.output_path: str = str(Path(output_path).absolute().resolve())

        def foo(s: str):
            with open(self.output_path, "a+") as f:
                f.write(s)

        super().__init__(foo, logger_id, channel)


class LoggerInput:
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
        for logger in LoggerOutput._loggers[channel]:
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
        cls._logger = LoggerInput(cls)
        cls._registered_loggers: List[LoggerOutput] = []
        cls.init_subscribers()

    @classmethod
    @property
    def logger(cls) -> LoggerInput:
        return cls._logger

    @classmethod
    def init_subscribers(cls):
        pass

    @classmethod
    def register_logger(cls, logger: LoggerOutput) -> None:
        cls._registered_loggers.append(logger)


class AutoAddPrintLogger:
    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls._logger = LoggerInput(cls)
        cls._registered_loggers: List[LoggerOutput] = []
        cls.init_subscribers()

    @classmethod
    @property
    def logger(cls) -> LoggerInput:
        return cls._logger

    @classmethod
    def init_subscribers(cls):
        cls.register_logger(PrintLoggerOutput(logger_id=cls.__qualname__))

    @classmethod
    def register_logger(cls, logger: LoggerOutput) -> None:
        cls._registered_loggers.append(logger)


__all__ = [
    "Logger",
    "LoggerOutput",
    "PrintLoggerOutput",
    "FIleLoggerOutput",
    "LoggerInput",
    "Logger",
    "AutoAddPrintLogger",
]
