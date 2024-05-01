from ..io_ import file_exists, delete_file
import atexit


class TemporaryFile:
    _instances: set['TemporaryFile'] = set()

    def __init__(self, path: str):
        if file_exists(path):
            raise RuntimeError(f"Can't create a temporary file if file '{path}' already exists.")
        self.path = path
        TemporaryFile._instances.add(self)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @atexit.register
    @staticmethod
    def _global_close():
        for inst in TemporaryFile._instances:
            inst.close()

    def close(self) -> None:
        delete_file(self.path)

    def read(self) -> list[str]:
        if not file_exists(self.path):
            return []
        with open(self.path, 'r') as f:
            return f.readlines()

    def write(self, lines: list[str]) -> None:
        with open(self.path, 'a') as f:
            f.writelines(lines)

    def clear(self):
        with open(self.path, 'w') as _:
            pass


__all__ = [
    'TemporaryFile'
]
