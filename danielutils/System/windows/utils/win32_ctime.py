"""
credit to https://github.com/Delgan/win32-setctime/blob/master/win32_setctime.py
and modifications by me
"""
from enum import IntEnum
import os

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


class CreationDisposition(IntEnum):
    # https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew
    CREATE_NEW = 1
    CREATE_ALWAYS = 2
    OPEN_EXISTING = 3
    OPEN_ALWAYS = 4
    TRUNCATE_EXISTING = 5


def epoch_time_to_windows_time(timestamp: int) -> int:
    # https://stackoverflow.com/questions/1566645/filetime-to-int64
    # https://stackoverflow.com/questions/6161776/convert-windows-filetime-to-second-in-unix-linux
    return int(timestamp * 10000000) + 116444736000000000


def windows_time_to_epoch(timestamp: int) -> int:
    # https://stackoverflow.com/questions/1566645/filetime-to-int64
    # https://stackoverflow.com/questions/6161776/convert-windows-filetime-to-second-in-unix-linux
    return (timestamp-116444736000000000)//10000000


def close_handle(handle) -> None:
    if not wintypes.BOOL(CloseHandle(handle)):
        raise WinError(get_last_error())


def setctime(filepath: str, timestamp, *, follow_symlinks: bool = True) -> None:
    """Set the "ctime" (creation time) attribute of a file given an unix timestamp (Windows only)."""
    if not SUPPORTED:
        raise OSError(
            "This function is only available for the Windows platform.")

    filepath = os.path.normpath(os.path.abspath(str(filepath)))
    timestamp = epoch_time_to_windows_time(timestamp)

    if not 0 < timestamp < (1 << 64):
        raise ValueError(
            "The system value of the timestamp exceeds u64 size: %d" % timestamp)

    atime = wintypes.FILETIME(0xFFFFFFFF, 0xFFFFFFFF)
    mtime = wintypes.FILETIME(0xFFFFFFFF, 0xFFFFFFFF)
    ctime = wintypes.FILETIME(timestamp & 0xFFFFFFFF, timestamp >> 32)

    flags = 128 | 0x02000000

    if not follow_symlinks:
        flags |= 0x00200000

    handle = wintypes.HANDLE(
        CreateFileW(
            filepath,
            256,
            0,
            None,
            CreationDisposition.OPEN_EXISTING.value,
            flags,
            None
        )
    )
    if handle.value == wintypes.HANDLE(-1).value:
        raise WinError(get_last_error())

    if not wintypes.BOOL(SetFileTime(handle, byref(ctime), byref(atime), byref(mtime))):
        raise WinError(get_last_error())
    close_handle(handle)


MaybeFileDescriptor = int


def getctime(filepath: str, follow_symlinks: bool = True) -> int:
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
                    CreationDisposition.OPEN_EXISTING.value, flags, None)
    handle = wintypes.HANDLE(f)
    if handle.value == wintypes.HANDLE(-1).value:
        raise WinError(get_last_error())

    if not wintypes.BOOL(GetFileTime(handle, byref(ctime), byref(atime), byref(mtime))):
        raise WinError(get_last_error())

    close_handle(handle)

    # reverse of calculation in setctime function above.
    # https://stackoverflow.com/questions/1566645/filetime-to-int64
    ctime64bit = ctime.dwHighDateTime << 32 | ctime.dwLowDateTime  # type:ignore
    # https://stackoverflow.com/questions/6161776/convert-windows-filetime-to-second-in-unix-linux
    return windows_time_to_epoch(ctime64bit)


__version__ = "1.1.0"
__all__ = [
    "setctime",
    "getctime"
]
