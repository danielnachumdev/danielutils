import atexit
import random
from typing import ContextManager, Set, List, Literal, Optional
from ..io_ import file_exists, delete_file


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
        return TemporaryFile(temp_name)

    def __init__(self, path: str):
        if file_exists(path):
            raise RuntimeError(f"Can't create a temporary file if file '{path}' already exists.")
        self.path = path
        TemporaryFile._instances.add(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __str__(self) -> str:
        return self.path

    def close(self) -> None:
        delete_file(self.path)

    def read(self) -> str:
        if not file_exists(self.path):
            return ""
        with open(self.path, 'r') as f:
            return f.read()

    def readlines(self) -> List[str]:
        if not file_exists(self.path):
            return []
        with open(self.path, 'r') as f:
            return f.readlines()

    def write(self, s: str) -> None:
        with open(self.path, 'a') as f:
            f.write(s)

    def writelines(self, lines: List[str]) -> None:
        with open(self.path, 'a') as f:
            f.writelines(lines)

    def clear(self):
        with open(self.path, 'w') as _:
            pass


@atexit.register
def __close_all():
    for inst in TemporaryFile._instances:  # type:ignore #pylint: disable=all
        inst.close()


__all__ = [
    'TemporaryFile'
]
