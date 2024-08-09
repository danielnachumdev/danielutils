import re
from dataclasses import dataclass
from typing import Optional, List

ARGUMENT_INFO_REGEX: re.Pattern = re.compile(
    r"(?P<kwargs>\*\*\w[\w\d]*)|(?P<args>\*(?:\w[\w\d]*)?)|(?P<kwarg_only>\/)|(?P<name>\w[\w\d]*)(?:(?:\s*:(?P<type>[^\=\n]+))?(?:\s*=(?P<default_value>[\s\S]+))?)?")


class ArgumentInfo:
    def __init__(self,
                 name: Optional[str],
                 type: Optional[str],
                 default: Optional[str],
                 is_kwargs: bool,
                 is_args: bool,
                 is_kwargs_only: bool):
        self._name = name
        self._type = type
        self._default = default
        self._is_kwargs = is_kwargs
        self._is_args = is_args
        self._is_kwargs_only = is_kwargs_only

    @property
    def name(self) -> Optional[str]:
        return self._name

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def default(self) -> Optional[str]:
        return self._default

    @property
    def is_kwargs(self) -> bool:
        return self._is_kwargs

    @property
    def is_args(self) -> bool:
        return self._is_args

    @property
    def is_kwargs_only(self) -> bool:
        return self._is_kwargs_only

    def __repr__(self) -> str:
        res = f"{self.__class__.__name__}(name=\"{self.name}\""
        if self.type is not None:
            res += f", type={self.type}"
        if self.default is not None:
            res += f", default={self.default}"

        return res + ")"

    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def _parse_one(string: str) -> 'ArgumentInfo':
        m = ARGUMENT_INFO_REGEX.match(string)
        if m is None:
            raise ValueError(f"Invalid argument info string: {string}")

        kwargs, args, kwarg_only, name, type, default_value = m.groups()
        return ArgumentInfo(
            name=name,
            type=type,
            default=default_value,
            is_kwargs=kwargs is not None,
            is_args=args is not None,
            is_kwargs_only=kwarg_only is not None,
        )

    @staticmethod
    def from_str(string: str) -> List['ArgumentInfo']:
        if string is None:
            return []
        string = string.strip()
        indices = [-1]
        stack: List[str] = []
        for i, c in enumerate(string):
            if len(stack) == 0:
                if c == ",":
                    indices.append(i)
            elif c in {'[', ']'}:
                if c == '[':
                    stack.append(c)
                else:
                    stack.pop()
        indices.append(len(string))
        res = []
        for start, end in zip(indices[:-1], indices[1:]):
            substr = string[start + 1:end].strip()
            res.append(ArgumentInfo._parse_one(substr))
        return res


__all__ = [
    "ArgumentInfo",
]
