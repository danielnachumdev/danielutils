import asyncio
from typing import Tuple, Optional


async def async_cmd(
        cmd: str,
        *,
        capture_stdout: bool = False,
        capture_stderr: bool = False
) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    kwargs = {}
    if capture_stdout:
        kwargs['stdout'] = asyncio.subprocess.PIPE
    if capture_stderr:
        kwargs['stderr'] = asyncio.subprocess.PIPE
    process = await asyncio.create_subprocess_shell(cmd, **kwargs)  # type:ignore
    stdout, stderr = await process.communicate()
    return process.returncode, stdout, stderr


__all__ = [
    'async_cmd',
]
