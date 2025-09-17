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
        logger.debug(f"Creating random temporary file: {temp_name}")
        return TemporaryFile(temp_name)

    def __init__(self, path: str):
        if file_exists(path):
            logger.error(f"Can't create temporary file - file already exists: {path}")
            raise RuntimeError(f"Can't create a temporary file if file '{path}' already exists.")
        self.path = path
        TemporaryFile._instances.add(self)
        logger.debug(f"TemporaryFile created: {path}")

    def __enter__(self):
        logger.debug(f"TemporaryFile context entered: {self.path}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning(f"TemporaryFile context exited with exception: {exc_type.__name__}: {exc_val}")
        else:
            logger.debug(f"TemporaryFile context exited successfully: {self.path}")
        self.close()

    def __str__(self) -> str:
        return self.path

    def close(self) -> None:
        logger.debug(f"Closing temporary file: {self.path}")
        delete_file(self.path)

    def read(self) -> str:
        if not file_exists(self.path):
            logger.debug(f"Temporary file does not exist for reading: {self.path}")
            return ""
        logger.debug(f"Reading temporary file: {self.path}")
        with open(self.path, 'r') as f:
            return f.read()

    def readbinary(self) -> bytes:
        if not file_exists(self.path):
            logger.debug(f"Temporary file does not exist for binary reading: {self.path}")
            return b""
        logger.debug(f"Reading temporary file as binary: {self.path}")
        with open(self.path, 'rb') as f:
            return f.read()

    def readlines(self) -> List[str]:
        if not file_exists(self.path):
            logger.debug(f"Temporary file does not exist for reading lines: {self.path}")
            return []
        logger.debug(f"Reading lines from temporary file: {self.path}")
        with open(self.path, 'r') as f:
            return f.readlines()

    def write(self, s: str) -> None:
        logger.debug(f"Writing to temporary file: {self.path}")
        with open(self.path, 'a') as f:
            f.write(s)

    def writebinary(self, s: bytes) -> None:
        logger.debug(f"Writing binary data to temporary file: {self.path}")
        with open(self.path, 'ab') as f:
            f.write(s)

    def writelines(self, lines: List[str]) -> None:
        logger.debug(f"Writing {len(lines)} lines to temporary file: {self.path}")
        with open(self.path, 'a') as f:
            f.writelines(lines)

    def clear(self):
        logger.debug(f"Clearing temporary file: {self.path}")
        with open(self.path, 'w') as _:
            pass


@atexit.register
def __close_all():
    logger.debug(f"Closing {len(TemporaryFile._instances)} temporary files at exit")
    for inst in TemporaryFile._instances:  # type:ignore #pylint: disable=all
        inst.close()


__all__ = [
    'TemporaryFile'
]
