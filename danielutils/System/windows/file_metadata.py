from typing import TypeAlias
from .utils.win32_ctime import getctime, setctime
from .utils.filetime import FileTime
EpochTime: TypeAlias = int


class FileMetadata:
    def __init__(self, path: str) -> None:
        self._path = path

    def get_creation_time(self) -> FileTime:
        return FileTime(getctime(self._path))

    def set_creation_time(self, filetime: FileTime) -> None:
        setctime(self._path, filetime.posix)
