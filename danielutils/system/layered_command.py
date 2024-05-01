import sys, os
from typing import Optional
from ..context_managers import TemporaryFile


class LayeredCommand:
    class_flush_stdout: bool = True
    class_raise_on_fail: bool = True
    class_verbose: bool = False
    _cls_prev_instance: Optional['LayeredCommand'] = None
    _id: int = 0

    def __init__(
            self,
            command: Optional[str] = None,
            instance_flush_stdout: Optional[bool] = None,
            instance_raise_on_fail: Optional[bool] = None,
            instance_verbose: Optional[bool] = None
    ):
        self._command = command if command is not None else ""
        self._instance_flush_stdout = instance_flush_stdout
        self._instance_raise_on_fail = instance_raise_on_fail
        self._instance_verbose = instance_verbose
        self._prev_instance = LayeredCommand._cls_prev_instance
        LayeredCommand._cls_prev_instance = self
        self._executor = os.system
        self._has_entered: bool = False

    def __enter__(self):
        self._has_entered = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LayeredCommand._cls_prev_instance = self._prev_instance

    def _build_command(self, *commands: str) -> str:
        res = ""
        if self._prev_instance is not None:
            prev = self._prev_instance._build_command()
            res += f"{prev} & " if prev != "" else ""
        if self._command != "":
            return res + " & ".join([self._command, *commands])
        return res + " & ".join(commands)

    def _error(self, predicate: bool, command: str, code: int, command_verbose: Optional[bool]) -> None:
        verbose = command_verbose if command_verbose is not None else (
            self._instance_verbose if self._instance_verbose is not None
            else LayeredCommand.class_verbose)
        if predicate:
            if verbose:
                raise RuntimeError(f"command '{command}' failed with exit code {code}")
            sys.exit(1)

    def execute(self, *commands: str, command_flush_stdout: Optional[bool] = None,
                command_raise_on_fail: bool = None, command_verbose: Optional[bool] = None) -> tuple[int, list[str]]:
        if not self._has_entered:
            raise RuntimeError(
                "LayeredCommand must be used with a context manager. Use as: `with LayeredCommand(...) as l1:`")
        command_flush_stdout = command_flush_stdout if command_flush_stdout is not None else (
            self._instance_flush_stdout if self._instance_flush_stdout is not None
            else LayeredCommand.class_flush_stdout)
        raise_on_fail = command_raise_on_fail if command_raise_on_fail is not None else (
            self._instance_raise_on_fail if self._instance_raise_on_fail is not None
            else LayeredCommand.class_raise_on_fail)

        command = self._build_command(*commands)
        if command_flush_stdout:
            code = self._executor(command)
            self._error(raise_on_fail and code != 0, command, code, command_verbose)
            return code, []

        temp_name = f"./alkjgaprgijfpeasjkegnrtlskdjfnbvlkajdertnbolrijk_{LayeredCommand._id}"
        LayeredCommand._id += 1
        with TemporaryFile(temp_name) as temp:
            command += f" >> {temp_name}"
            code = self._executor(command)
            self._error(raise_on_fail and code != 0, command, code, command_verbose)
            return code, temp.read()

    def __call__(self, *args, **kwargs) -> tuple[int, list[str]]:
        return self.execute(*args, **kwargs)


__all__ = [
    'LayeredCommand'
]
