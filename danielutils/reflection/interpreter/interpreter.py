import os
import sys
from typing import Any


class Interpreter:
    def get_version(self):
        pass

    def __init__(self, executable_path: str) -> None:
        self._executable_path = executable_path

    def _execute(self, command: str) -> None:
        os.system(command)

    def run_module(self, module_name: str, *args, **kwargs) -> None:
        jargs = " ".join(args)
        jkwargs = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        self._execute(f'{self._executable_path} -m {module_name} {jargs} {jkwargs}')

    def execute_file(self, file_name: str, *args, **kwargs) -> None:
        jargs = " ".join(args)
        jkwargs = " ".join([f"{k}={v}" for k, v in kwargs.items()])
        self._execute(f'{self._executable_path} {file_name} {jargs} {jkwargs}')

    def execute_package(self, package_name: str, *args, **kwargs) -> None:
        self.execute_file(package_name, *args, **kwargs)

    def evaluate(self, expr: str) -> Any:
        return self._execute(f"{self._executable_path} -c {expr}")


class CurrentInterpreter(Interpreter):
    def __init__(self) -> None:
        super().__init__(sys.executable)


__all__ = [
    "Interpreter",
    "CurrentInterpreter",
]
