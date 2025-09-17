import logging
from pathlib import Path

from ....io_ import delete_file, directory_exists, create_directory
from ...utils import get_logger
from ..logger_strategy_impl_base import LoggerStrategyImplBase

logger = get_logger(__name__)


class FIleLogger(LoggerStrategyImplBase):
    def __init__(self, output_path: str, logger_id: str, delete_if_already_exists: bool = True, channel: str = "all"):
        logger.info("Initializing FileLogger: path=%s, id=%s, delete_existing=%s, channel=%s", output_path, logger_id, delete_if_already_exists, channel)
        
        if delete_if_already_exists:
            delete_file(output_path)
        
        parent = str(Path(output_path).parent.absolute().resolve())
        if not directory_exists(parent):
            logger.info("Creating parent directory: %s", parent)
            create_directory(parent)
        
        self.output_path: str = str(Path(output_path).absolute().resolve())

        def foo(s: str):
            with open(self.output_path, "a+") as f:
                f.write(s)

        super().__init__(foo, logger_id, channel)
        logger.info("FileLogger %s initialized successfully", logger_id)


__all__ = [
    "FIleLogger"
]
