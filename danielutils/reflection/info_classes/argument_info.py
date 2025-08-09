import re
from dataclasses import dataclass
from typing import Optional, List

ARGUMENT_INFO_REGEX: re.Pattern = re.compile(
    r"(?P<kwargs>\*\*\w[\w\d]*)|(?P<args>\*(?:\w[\w\d]*)?)|(?P<kwarg_only>\/)|(?P<pname>\w[\w\d]*)\[(?P<parameters>.+)\]|(?P<name>\w[\w\d]*)(?:(?:\s*:(?P<type>[^\=\n]+))?(?:\s*=(?P<default_value>[\s\S]+))?)?")


class ArgumentInfo:
    def __init__(self,
                 name: Optional[str],
                 type: Optional[str],
                 default: Optional[str],
                 is_kwargs: bool,
                 is_args: bool,
                 is_kwargs_only: bool,
                 parameters: Optional[List]):
        self._name = name
        self._type = type
        self._default = default
        self._is_kwargs = is_kwargs
        self._is_args = is_args
        self._is_kwargs_only = is_kwargs_only
        self._parameters = parameters

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

    @property
    def parameters(self) -> Optional[List]:
        return self._parameters

    @property
    def is_parameterized(self) -> bool:
        return self._parameters is not None and len(self.parameters) > 0  # type: ignore

    def __repr__(self) -> str:
        res = f"{self.__class__.__name__}(name=\"{self.name}\""
        if self.type is not None:
            res += f", type={self.type}"
        if self.default is not None:
            res += f", default={self.default}"
        if self.is_parameterized:
            res += f", parameters={self.parameters}"
        return res + ")"

    def __str__(self) -> str:
        return repr(self)

    @staticmethod
    def _parse_one(string: str) -> 'ArgumentInfo':
        m = ARGUMENT_INFO_REGEX.match(string)
        if m is None:
            raise ValueError(f"Invalid argument info string: {string}")

        kwargs, args, kwarg_only, pname, parameters, name, type, default_value = m.groups()
        type = None if type is None else type.strip()
        default_value = None if default_value is None else default_value.strip()
        return ArgumentInfo(
            name=name or pname or (args.strip("*") if args else None) or (
                kwargs.strip("*") if kwargs else None) or (kwarg_only.strip("/") if kwarg_only else None) or None,
            type=type,
            default=default_value,
            is_kwargs=kwargs is not None,
            is_args=args is not None,
            is_kwargs_only=kwarg_only is not None,
            parameters=[parameters]
        )

    @staticmethod
    def from_str(string: str) -> List['ArgumentInfo']:
        if string is None:
            return []
        string = string.strip()
        if not string:
            return []
        string = string.strip()
        indices = [-1]
        stack: List[str] = []
        for i, c in enumerate(string):
            if c in {'[', ']'}:
                if c == '[':
                    stack.append(c)
                else:
                    stack.pop()
            elif len(stack) == 0:
                if c == ",":
                    indices.append(i)
        indices.append(len(string))
        res = []
        for start, end in zip(indices[:-1], indices[1:]):
            substr = string[start + 1:end].strip()
            res.append(ArgumentInfo._parse_one(substr))
        return res


__all__ = [
    "ArgumentInfo",
]
