import logging
import sys, os
from typing import Optional, Tuple, List
from ..context_managers import TemporaryFile
import random
from ..logging_.utils import get_logger

logger = get_logger(__name__)


class LayeredCommand:
    class_capture_stdout: bool = True
    class_capture_stderr: bool = True
    class_raise_on_fail: bool = False
    class_verbose: bool = False
    _class_prev_instance: Optional['LayeredCommand'] = None
    _id: int = 0

    @property
    def prev(self):
        return self._prev_instance

    @prev.setter
    def prev(self, value: Optional['LayeredCommand'] = None):
        self._prev_instance = value

    def __init__(
            self,
            command: Optional[str] = None,
            *,
            prev_instance: Optional['LayeredCommand'] = None,
            instance_capture_stdout: Optional[bool] = None,
            instance_capture_stderr: Optional[bool] = None,
            instance_raise_on_fail: Optional[bool] = None,
            instance_verbose: Optional[bool] = None
    ):
        self._command = command if command is not None else ""
        self._instance_capture_stdout = instance_capture_stdout
        self._instance_capture_stderr = instance_capture_stderr
        self._instance_raise_on_fail = instance_raise_on_fail
        self._instance_verbose = instance_verbose
        self._prev_instance = prev_instance if prev_instance is not None else LayeredCommand._class_prev_instance
        self._cur_class_prev_instance = LayeredCommand._class_prev_instance
        LayeredCommand._class_prev_instance = self
        self._executor = os.system
        self._has_entered: bool = False
        logger.info("LayeredCommand initialized with command: '%s', prev_instance: %s", self._command, prev_instance is not None)

    def __enter__(self):
        self._open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logger.warning("LayeredCommand context exited with exception: %s: %s", exc_type.__name__, exc_val)
        if self.prev is self._cur_class_prev_instance:
            LayeredCommand._class_prev_instance = self.prev

    def _open(self) -> None:
        self._has_entered = True

    def _build_command(self, *commands: str) -> str:
        res = ""
        if self.prev is not None:
            prev = self.prev._build_command()
            res += f"{prev} & " if prev != "" else ""
        if self._command != "":
            return res + " & ".join([self._command, *commands])
        return res + " & ".join(commands)

    def _error(self, predicate: bool, command: str, code: int, command_verbose: Optional[bool]) -> None:
        if predicate:
            verbose = self._merge_values(command_verbose, self._instance_verbose, LayeredCommand.class_verbose)
            if verbose:
                raise RuntimeError(f"command '{command}' failed with exit code {code}")
            sys.exit(1)

    @staticmethod
    def _merge_values(command: Optional[bool], instance: Optional[bool], class_: bool) -> bool:
        return command if command is not None else (instance if instance is not None else class_)

    def execute(
            self,
            *commands: str,
            command_capture_stdout: Optional[bool] = None,
            command_capture_stderr: Optional[bool] = None,
            command_raise_on_fail: Optional[bool] = None,
            command_verbose: Optional[bool] = None
    ) -> Tuple[int, List[str], List[str]]:
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
        logger.info("Executing command: %s", command)
        
        if not capture_stdout and not capture_stderr:
            code = self._executor(command)
            self._error(raise_on_fail and code != 0, command, code, command_verbose)
            return code, [], []

        letters = "abcdefghijklmnopqrstuvwxyz"
        prefix = "".join(random.choices(letters, k=10)) + f"_{LayeredCommand._id}"
        LayeredCommand._id += 1
        
        with TemporaryFile.random(prefix=prefix, suffix="stdout.log") as stdout:
            with TemporaryFile.random(prefix=prefix, suffix="stderr.log") as stderr:
                if capture_stdout:
                    command += f" > {stdout}"
                if capture_stderr:
                    command += f" 2> {stderr}"
                code = self._executor(command)
                self._error(raise_on_fail and code != 0, command, code, command_verbose)
                return code, stdout.readlines(), stderr.readlines()

    def __call__(self, *args, **kwargs) -> Tuple[int, List[str], List[str]]:
        return self.execute(*args, **kwargs)


__all__ = [
    'LayeredCommand'
]
