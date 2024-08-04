import atexit
import random
from typing import ContextManager, Set, List, Literal
from ..io_ import file_exists, delete_file


class TemporaryFile(ContextManager):
    _instances: Set['TemporaryFile'] = set()

    @classmethod
    def random(cls, type: Literal["file", "folder"]) -> 'TemporaryFile':
        letters = "abcdefghijklmnopqrstuvwxyz"
        temp_name = f"{type}_" + "".join(random.choices(letters, k=50))
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

    def close(self) -> None:
        delete_file(self.path)

    def read(self) -> List[str]:
        if not file_exists(self.path):
            return []
        with open(self.path, 'r') as f:
            return f.readlines()

    def write(self, lines: List[str]) -> None:
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
