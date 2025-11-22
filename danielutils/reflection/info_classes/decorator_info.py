import re
from dataclasses import dataclass, Field
from typing import Optional, List

from .argument_info import ArgumentInfo


class DecoratorInfo:
    DECORATOR_INFO_REGEX: re.Pattern = re.compile(
        r"^@?(?P<name>\w[\w\d]*)(?:\((?P<arguments>.*)\))?$")

    def __init__(self, name: str, arguments: List[ArgumentInfo]):
        self._name = name
        self._arguments = arguments

    @property
    def name(self) -> str:
        return self._name

    @property
    def arguments(self) -> List[ArgumentInfo]:
        return self._arguments

    @staticmethod
    def from_str(string: str) -> 'DecoratorInfo':
        m = DecoratorInfo.DECORATOR_INFO_REGEX.match(string)
        if m is None:
            raise ValueError(f"Invalid decorator format: {repr(string)}")

        name, arguments = m.groups()
        if arguments:
            try:
                args = ArgumentInfo.from_str(arguments)
            except ValueError as e:
                raise ValueError(
                    f"Failed to parse arguments for decorator '{name}': {e}\n"
                    f"Arguments string: {repr(arguments)}"
                ) from e
        else:
            args = []
        return DecoratorInfo(name, args)

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        if self.arguments:
            return f"{self.__class__.__name__}(name=\"{self.name}\", arguments={self.arguments})"
        return f"{self.__class__.__name__}(name=\"{self.name}\")"


__all__ = [
    'DecoratorInfo',
]
