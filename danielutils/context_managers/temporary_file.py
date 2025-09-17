import atexit
import logging
import random
from typing import ContextManager, Set, List, Literal, Optional
from ..io_ import file_exists, delete_file
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class TemporaryFile(ContextManager):
    _instances: Set['TemporaryFile'] = set()

    @classmethod
    def random(cls, length: int = 10, /, type: Literal["file", "folder"] = "file", prefix: Optional[str] = None,
               suffix: Optional[str] = None) -> 'TemporaryFile':
        from danielutils import RandomDataGenerator
        temp_name = f"{type}_"
        if prefix is not None:
            temp_name += f"{prefix}_"

        temp_name += RandomDataGenerator.name(length)
        if suffix is not None:
            temp_name += f"_{suffix}"
        logger.debug("Creating random temporary file: %s", temp_name)
        return TemporaryFile(temp_name)

    def __init__(self, path: str):
        if file_exists(path):
            logger.error("Can't create temporary file - file already exists: %s", path)
            raise RuntimeError(f"Can't create a temporary file if file '{path}' already exists.")
        self.path = path
        TemporaryFile._instances.add(self)
        logger.debug("TemporaryFile created: %s", path)

    def __enter__(self):
        logger.debug("TemporaryFile context entered: %s", self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning("TemporaryFile context exited with exception: %s: %s", exc_type.__name__, exc_val)
        else:
            logger.debug("TemporaryFile context exited successfully: %s", self.path)
        self.close()

    def __str__(self) -> str:
        return self.path

    def close(self) -> None:
        logger.debug("Closing temporary file: %s", self.path)
        delete_file(self.path)

    def read(self) -> str:
        if not file_exists(self.path):
            logger.debug("Temporary file does not exist for reading: %s", self.path)
            return ""
        logger.debug("Reading temporary file: %s", self.path)
        with open(self.path, 'r') as f:
            return f.read()

    def readbinary(self) -> bytes:
        if not file_exists(self.path):
            logger.debug("Temporary file does not exist for binary reading: %s", self.path)
            return b""
        logger.debug("Reading temporary file as binary: %s", self.path)
        with open(self.path, 'rb') as f:
            return f.read()

    def readlines(self) -> List[str]:
        if not file_exists(self.path):
            logger.debug("Temporary file does not exist for reading lines: %s", self.path)
            return []
        logger.debug("Reading lines from temporary file: %s", self.path)
        with open(self.path, 'r') as f:
            return f.readlines()

    def write(self, s: str) -> None:
        logger.debug("Writing to temporary file: %s", self.path)
        with open(self.path, 'a') as f:
            f.write(s)

    def writebinary(self, s: bytes) -> None:
        logger.debug("Writing binary data to temporary file: %s", self.path)
        with open(self.path, 'ab') as f:
            f.write(s)

    def writelines(self, lines: List[str]) -> None:
        logger.debug("Writing %s lines to temporary file: %s", len(lines), self.path)
        with open(self.path, 'a') as f:
            f.writelines(lines)

    def clear(self):
        logger.debug("Clearing temporary file: %s", self.path)
        with open(self.path, 'w') as _:
            pass


@atexit.register
def __close_all():
    logger.debug("Closing %s temporary files at exit", len(TemporaryFile._instances))
    for inst in TemporaryFile._instances:  # type:ignore #pylint: disable=all
        inst.close()


__all__ = [
    'TemporaryFile'
]
