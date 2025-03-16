import inspect
import json
import re
from typing import Type, Optional, List, Callable
from .decoration_info import DecorationInfo
from .argument_info import ArgumentInfo


class FunctionInfo:
    FUNCTION_DEFINITION_REGEX: re.Pattern = re.compile(
        r"(?P<decorators>[\s\S]+)?\s*def (?P<name>\w[\w\d]*)\s*\((?P<arguments>.+)?\)\s*(?:\s*\-\>\s*(?P<return_type>[\s\S]+?)\s*)?:(?P<body>[\s\S]+)",
        re.MULTILINE)

    def __init__(self, func: Callable, owner: Type) -> None:
        try:
            if inspect.isdatadescriptor(func):
                inspect.getsource(func.fget)  # type: ignore
                self._is_property = True
            else:
                inspect.getsource(func)
                self._is_property = False
        except:
            raise TypeError(f"'{func.__name__}' is not a user defined function")
        self._func = func
        self._decorators: List[DecorationInfo] = []
        self._arguments: List[ArgumentInfo] = []
        self._return_type: str = ""
        self._owner = owner
        self._parse_src_code()

    def _parse_src_code(self) -> None:
        f = self._func if not self.is_property else self._func.fget  # type:ignore
        code = inspect.getsource(f).strip()
        m = FunctionInfo.FUNCTION_DEFINITION_REGEX.match(code)
        if m is None:
            raise ValueError("Invalid function source code")
        decorators, name, arguments, return_type, body = m.groups()
        if decorators is not None:
            for substr in decorators.strip().splitlines():
                self._decorators.append(DecorationInfo.from_str(substr.strip()))
        self._name = name
        if arguments is not None:
            self._arguments = ArgumentInfo.from_str(arguments)

        self._return_type = "None"
        if return_type is not None:
            self._return_type = return_type

    def __str__(self) -> str:
        # body = json.dumps({
        #     "name": self.name,
        #     "decorators": self.decorators,
        #     "arguments": self.arguments
        # }, default=str, indent=4)
        return f"{self.__class__.__name__}(name=\"{self.name}\", decorators={self.decorators}, arguments={self.arguments})"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name=\"{self.name}\")"

    @property
    def is_inherited(self) -> bool:
        return self._func in set(self._owner.__dict__.keys())

    @property
    def is_class_method(self) -> bool:
        return "classmethod" in set(d.name for d in self.decorators)

    @property
    def is_static_method(self) -> bool:
        return "staticmethod" in set(d.name for d in self.decorators)

    @property
    def is_instance_method(self) -> bool:
        return not self.is_class_method and not self.is_static_method

    @property
    def is_abstract(self) -> bool:
        return getattr(self._func, '__isabstractmethod__', False)

    @property
    def is_property(self) -> bool:
        return self._is_property

    @property
    def name(self) -> str:
        return self._name

    @property
    def return_type(self) -> str:
        return self._return_type

    @property
    def arguments(self) -> List[ArgumentInfo]:
        return self._arguments

    @property
    def decorators(self) -> List[DecorationInfo]:
        return self._decorators


__all__ = [
    "FunctionInfo",
]
