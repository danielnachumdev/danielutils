"""
credit to https://github.com/Delgan/win32-setctime/blob/master/win32_setctime.py
and modifications by me
"""
from typing import Optional
from datetime import datetime
from enum import IntEnum
import os
from .utils import FileTime

try:
    from ctypes import byref, get_last_error, wintypes, WinDLL, WinError

    kernel32 = WinDLL("kernel32", use_last_error=True)

    CreateFileW = kernel32.CreateFileW
    SetFileTime = kernel32.SetFileTime
    # Modification
    GetFileTime = kernel32.GetFileTime
    CloseHandle = kernel32.CloseHandle

    CreateFileW.argtypes = (
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    CreateFileW.restype = wintypes.HANDLE

    SetFileTime.argtypes = (
        wintypes.HANDLE,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
        wintypes.PFILETIME,
    )
    SetFileTime.restype = wintypes.BOOL

    # modification
    # https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getfiletime
    GetFileTime.argtypes = (
        wintypes.HANDLE,
        wintypes.LPFILETIME,
        wintypes.LPFILETIME,
        wintypes.LPFILETIME,
    )
    GetFileTime.restype = wintypes.BOOL

    CloseHandle.argtypes = (wintypes.HANDLE,)
    CloseHandle.restype = wintypes.BOOL
except (ImportError, AttributeError, OSError, ValueError):
    SUPPORTED = False
else:
    SUPPORTED = os.name == "nt"


class HELPERS:

    class CreationDisposition(IntEnum):
        # https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew
        CREATE_NEW = 1
        CREATE_ALWAYS = 2
        OPEN_EXISTING = 3
        OPEN_ALWAYS = 4
        TRUNCATE_EXISTING = 5

    @staticmethod
    def epoch_time_to_windows_time(timestamp: float) -> int:
        # https://stackoverflow.com/questions/1566645/filetime-to-int64
        # https://stackoverflow.com/questions/6161776/convert-windows-filetime-to-second-in-unix-linux
        return int(timestamp * 10000000) + 116444736000000000

    @staticmethod
    def windows_time_to_epoch(timestamp: int) -> int:
        # https://stackoverflow.com/questions/1566645/filetime-to-int64
        # https://stackoverflow.com/questions/6161776/convert-windows-filetime-to-second-in-unix-linux
        return (timestamp-116444736000000000)//10000000

    @staticmethod
    def close_handle(handle) -> None:
        if not wintypes.BOOL(CloseHandle(handle)):
            raise WinError(get_last_error())

    @staticmethod
    def datetime_to_wintypes_FILETIME(dt: Optional[datetime]) -> 'wintypes.FILETIME':
        if dt is None:
            return wintypes.FILETIME(0xFFFFFFFF, 0xFFFFFFFF)

        timestamp = HELPERS.epoch_time_to_windows_time(dt.timestamp())
        if not 0 < timestamp < (1 << 64):
            raise ValueError(
                "The system value of the timestamp exceeds u64 size: %d" % timestamp)

        return wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)


def setctime(filepath: str, filetime: FileTime, *, follow_symlinks: bool = True) -> None:
    """Set the "ctime" (creation time) attribute of a file given an unix timestamp (Windows only)."""
    if not SUPPORTED:
        raise OSError(
            "This function is only available for the Windows platform.")

    if filetime.access is None and filetime.modification is None and filetime.creation is None:
        raise ValueError(
            "This function has no meaning if all values in 'filetime' argument are None. This is probably a mistake")

    filepath = os.path.normpath(os.path.abspath(str(filepath)))

    atime: wintypes.FILETIME = HELPERS.datetime_to_wintypes_FILETIME(
        filetime.access)
    mtime: wintypes.FILETIME = HELPERS.datetime_to_wintypes_FILETIME(
        filetime.modification)
    ctime: wintypes.FILETIME = HELPERS.datetime_to_wintypes_FILETIME(
        filetime.creation)

    flags = 128 | 0x02000000

    if not follow_symlinks:
        flags |= 0x00200000

    handle = wintypes.HANDLE(
        CreateFileW(
            filepath,
            256,
            0,
            None,
            HELPERS.CreationDisposition.OPEN_EXISTING.value,
            flags,
            None
        )
    )
    if handle.value == wintypes.HANDLE(-1).value:
        raise WinError(get_last_error())

    if not wintypes.BOOL(SetFileTime(handle, byref(ctime), byref(atime), byref(mtime))):
        raise WinError(get_last_error())
    HELPERS.close_handle(handle)


def getctime(filepath: str, follow_symlinks: bool = True) -> FileTime:
    if not SUPPORTED:
        raise OSError(
            "This function is only available for the Windows platform.")

    filepath = os.path.normpath(os.path.abspath(str(filepath)))

    # placeholder variables to hold values for
    atime = wintypes.FILETIME()  # last access time
    mtime = wintypes.FILETIME()  # last modification time
    ctime = wintypes.FILETIME()  # creation time

    flags = 128 | 0x02000000

    if not follow_symlinks:
        flags |= 0x00200000
    f = CreateFileW(filepath, 256, 0, None,
                    HELPERS.CreationDisposition.OPEN_EXISTING.value, flags, None)
    handle = wintypes.HANDLE(f)
    if handle.value == wintypes.HANDLE(-1).value:
        raise WinError(get_last_error())

    if not wintypes.BOOL(GetFileTime(handle, byref(ctime), byref(atime), byref(mtime))):
        raise WinError(get_last_error())

    HELPERS.close_handle(handle)

    # reverse of calculation in setctime function above.
    stage1 = map(
        lambda time: time.dwHighDateTime << 32 | time.dwLowDateTime,  # type:ignore
        [ctime, mtime, atime]
    )
    stage2 = map(HELPERS.windows_time_to_epoch, stage1)
    stage3 = map(datetime.fromtimestamp, stage2)
    return FileTime(*list(stage3))


__all__ = [
    "setctime",
    "getctime",
    'FileTime'
]
