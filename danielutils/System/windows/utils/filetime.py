from datetime import datetime
from ....Time import epoch_to_datetime, datetime_to_epoch


class FileTime:

    @staticmethod
    def from_datatime(dt: datetime) -> 'FileTime':
        return FileTime(FileTime.datetime_to_epoch(dt))

    def __init__(self, posix_timestamp: float) -> None:
        self._timestamp = posix_timestamp
        self._datetime = FileTime.epoch_to_datetime(self._timestamp)

    @property
    def posix(self) -> float:
        return self._timestamp

    @property
    def datetime(self) -> datetime:
        return self._datetime

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.datetime})"

    epoch_to_datetime = staticmethod(epoch_to_datetime)
    datetime_to_epoch = staticmethod(datetime_to_epoch)
