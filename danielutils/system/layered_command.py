import sys, os
from typing import Optional
from ..context_managers import TemporaryFile
import random


class LayeredCommand:
    class_flush_stdout: bool = True
    class_flush_stderr: bool = True
    class_raise_on_fail: bool = True
    class_verbose: bool = False
    _class_prev_instance: Optional['LayeredCommand'] = None
    _id: int = 0

    def __init__(
            self,
            command: Optional[str] = None,
            *,
            prev_instance: Optional['LayeredCommand'] = None,
            instance_flush_stdout: Optional[bool] = None,
            instance_flush_stderr: Optional[bool] = None,
            instance_raise_on_fail: Optional[bool] = None,
            instance_verbose: Optional[bool] = None
    ):
        self._command = command if command is not None else ""
        self._instance_flush_stdout = instance_flush_stdout
        self._instance_flush_stderr = instance_flush_stderr
        self._instance_raise_on_fail = instance_raise_on_fail
        self._instance_verbose = instance_verbose
        self._prev_instance = prev_instance if prev_instance is not None else LayeredCommand._class_prev_instance
        self._cur_class_prev_instance = LayeredCommand._class_prev_instance
        LayeredCommand._class_prev_instance = self
        self._executor = os.system
        self._has_entered: bool = False

    def __enter__(self):
        self._open()
        return self

    def _open(self) -> None:
        self._has_entered = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._prev_instance is self._cur_class_prev_instance:
            LayeredCommand._class_prev_instance = self._prev_instance

    def _build_command(self, *commands: str) -> str:
        res = ""
        if self._prev_instance is not None:
            prev = self._prev_instance._build_command()
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
            command_flush_stdout: Optional[bool] = None,
            command_flush_stderr: Optional[bool] = None,
            command_raise_on_fail: Optional[bool] = None,
            command_verbose: Optional[bool] = None
    ) -> tuple[int, list[str], list[str]]:
        if not self._has_entered:
            raise RuntimeError(
                "LayeredCommand must be used with a context manager. Use as: `with LayeredCommand(...) as l1:`")
        flush_stdout = self._merge_values(command_flush_stdout, self._instance_flush_stdout, self.class_flush_stdout)
        flush_stderr = self._merge_values(command_flush_stderr, self._instance_flush_stderr, self.class_flush_stderr)
        raise_on_fail = self._merge_values(command_raise_on_fail, self._instance_raise_on_fail,
                                           self.class_raise_on_fail)

        command = self._build_command(*commands)
        if flush_stdout and flush_stderr:
            code = self._executor(command)
            self._error(raise_on_fail and code != 0, command, code, command_verbose)
            return code, [], []

        letters = "abcdefghijklmnopqrstuvwxyz"
        temp_name = "".join(random.choices(letters, k=50)) + f"_{LayeredCommand._id}"
        stdout_path = f"./{temp_name}_stdout.log"
        stderr_path = f"./{temp_name}_stderr.log"
        LayeredCommand._id += 1
        with TemporaryFile(stdout_path) as stdout:
            with TemporaryFile(stderr_path) as stderr:
                if not flush_stdout:
                    command += f" > {stdout_path}"
                if not flush_stderr:
                    command += f" 2> {stderr_path}"
                code = self._executor(command)
                self._error(raise_on_fail and code != 0, command, code, command_verbose)
                return code, stdout.read(), stderr.read()

    def __call__(self, *args, **kwargs) -> tuple[int, list[str], list[str]]:
        return self.execute(*args, **kwargs)


__all__ = [
    'LayeredCommand'
]
