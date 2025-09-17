import asyncio
import logging
from typing import Tuple, Optional
from ..logging_.utils import get_logger
logger = get_logger(__name__)


async def async_cmd(
        cmd: str,
        *,
        capture_stdout: bool = False,
        capture_stderr: bool = False
) -> Tuple[int, Optional[bytes], Optional[bytes]]:
    logger.debug("Executing async command: %s, capture_stdout=%s, capture_stderr=%s", cmd, capture_stdout, capture_stderr)
    kwargs = {}
    if capture_stdout:
        kwargs['stdout'] = asyncio.subprocess.PIPE
    if capture_stderr:
        kwargs['stderr'] = asyncio.subprocess.PIPE
    process = await asyncio.create_subprocess_shell(cmd, **kwargs)  # type:ignore
    stdout, stderr = await process.communicate()
    logger.debug("Command completed with returncode=%s", process.returncode)
    return process.returncode, stdout, stderr


__all__ = [
    'async_cmd',
]
