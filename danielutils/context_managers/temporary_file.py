from ..io_ import file_exists, delete_file


class TemporaryFile:
    def __init__(self, path: str):
        if file_exists(path):
            raise RuntimeError(f"Can't create a temporary file if file '{path}' already exists.")
        self.path = path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self) -> None:
        delete_file(self.path)

    def read(self) -> list[str]:
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
