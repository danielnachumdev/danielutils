import sys
import logging
from typing import Optional, Tuple, List

from .async_cmd import async_cmd
from ..logging_.utils import get_logger
logger = get_logger(__name__)


class AsyncLayeredCommand:
    class_capture_stdout: bool = True
    class_capture_stderr: bool = True
    class_raise_on_fail: bool = False
    class_verbose: bool = False
    _class_prev_instance: Optional['AsyncLayeredCommand'] = None
    _id: int = 0

    @property
    def prev(self):
        return self._prev_instance

    @prev.setter
    def prev(self, value: Optional['AsyncLayeredCommand'] = None):
        self._prev_instance = value

    def __init__(
            self,
            command: Optional[str] = None,
            *,
            prev_instance: Optional['AsyncLayeredCommand'] = None,
            instance_capture_stdout: Optional[bool] = None,
            instance_capture_stderr: Optional[bool] = None,
            instance_raise_on_fail: Optional[bool] = None,
            instance_verbose: Optional[bool] = None
    ):
        logger.debug(f"Initializing AsyncLayeredCommand with command='{command}', prev_instance={prev_instance is not None}")
        self._command = command if command is not None else ""
        self._instance_capture_stdout = instance_capture_stdout
        self._instance_capture_stderr = instance_capture_stderr
        self._instance_raise_on_fail = instance_raise_on_fail
        self._instance_verbose = instance_verbose
        self._prev_instance = prev_instance if prev_instance is not None else AsyncLayeredCommand._class_prev_instance
        self._cur_class_prev_instance = AsyncLayeredCommand._class_prev_instance
        AsyncLayeredCommand._class_prev_instance = self
        self._has_entered: bool = False
        logger.debug(f"AsyncLayeredCommand initialized successfully")

    def __enter__(self):
        logger.debug("Entering AsyncLayeredCommand context")
        self._open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug(f"Exiting AsyncLayeredCommand context, exc_type={exc_type}")
        if self.prev is self._cur_class_prev_instance:
            AsyncLayeredCommand._class_prev_instance = self.prev

    def _open(self) -> None:
        logger.debug("Opening AsyncLayeredCommand")
        self._has_entered = True

    def _build_command(self, *commands: str) -> str:
        logger.debug(f"Building command with {len(commands)} additional commands")
        res = ""
        if self.prev is not None:
            prev = self.prev._build_command()
            res += f"{prev} & " if prev != "" else ""
        if self._command != "":
            result = res + " & ".join([self._command, *commands])
        else:
            result = res + " & ".join(commands)
        logger.debug(f"Built command: {result}")
        return result

    def _error(self, predicate: bool, command: str, code: int, command_verbose: Optional[bool]) -> None:
        if predicate:
            logger.error(f"Command '{command}' failed with exit code {code}")
            verbose = self._merge_values(command_verbose, self._instance_verbose, AsyncLayeredCommand.class_verbose)
            if verbose:
                raise RuntimeError(f"command '{command}' failed with exit code {code}")
            sys.exit(1)

    @staticmethod
    def _merge_values(command: Optional[bool], instance: Optional[bool], class_: bool) -> bool:
        return command if command is not None else (instance if instance is not None else class_)

    async def execute(
            self,
            *commands: str,
            command_capture_stdout: Optional[bool] = None,
            command_capture_stderr: Optional[bool] = None,
            command_raise_on_fail: Optional[bool] = None,
            command_verbose: Optional[bool] = None
    ) -> Tuple[int, List[str], List[str]]:
        logger.info(f"Executing AsyncLayeredCommand with {len(commands)} commands")
        if not self._has_entered:
            logger.error("LayeredCommand must be used with a context manager")
            raise RuntimeError(
                "LayeredCommand must be used with a context manager. Use as: `with LayeredCommand(...) as l1:`")
        capture_stdout = self._merge_values(command_capture_stdout, self._instance_capture_stdout,
                                            self.class_capture_stdout)
        capture_stderr = self._merge_values(command_capture_stderr, self._instance_capture_stderr,
                                            self.class_capture_stderr)
        raise_on_fail = self._merge_values(command_raise_on_fail, self._instance_raise_on_fail,
                                           self.class_raise_on_fail)

        command = self._build_command(*commands)
        logger.debug(f"Executing command with capture_stdout={capture_stdout}, capture_stderr={capture_stderr}")
        if not capture_stdout and not capture_stderr:
            code = (await async_cmd(command))[0]
            logger.debug(f"Command executed with return code {code}")
            self._error(raise_on_fail and code != 0, command, code, command_verbose)
            return code, [], []

        code, stdout, stderr = await async_cmd(command, capture_stdout=True, capture_stderr=True)
        logger.info(f"Command execution completed with return code {code}")
        return code, stdout.decode().splitlines() if stdout else [], stderr.decode().splitlines() if stderr else []

    async def __call__(self, *args, **kwargs) -> Tuple[int, List[str], List[str]]:
        return await self.execute(*args, **kwargs)


__all__ = [
    'AsyncLayeredCommand'
]
