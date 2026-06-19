import inspect
import re
from dataclasses import dataclass
from typing import Any, List, Optional, Protocol, Tuple, Type, Union

from .interpreter import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as List, tuple as Tuple  # type:ignore

argument_kwargs = dict(frozen=True)
function_declaration_kwargs = dict(frozen=True)
if get_python_version() >= (3, 10):
    argument_kwargs.update(slots=True)
    function_declaration_kwargs.update(slots=True)


def get_explicitly_declared_functions(cls: type) -> List[str]:
    return [func for func, _ in inspect.getmembers(cls, predicate=inspect.isfunction)]


def get_mro(obj: Any) -> List[type]:
    if isinstance(obj, type):
        return obj.mro()
    return get_mro(obj.__class__)


@dataclass(**argument_kwargs)
class Argument:
    name: str
    type: Optional[str]
    default: Optional[str]

    def __hash__(self) -> int:
        arg_type = self.type
        if self.type is not None and "Union" in self.type:
            arg_type = tuple(sorted(self.type[self.type.index("[") + 1:self.type.rindex("]")].split(",")))
        return hash((self.name, arg_type, self.default))

    def duplicate(self, **override_kwargs) -> 'Argument':
        data = dict(name=self.name, type=self.type, default=self.default)
        data.update(override_kwargs)
        return Argument(**data)


func_pattern = re.compile(
    r"(.*def[\s\\]*?(\w+)[\s\\]*?\(([\w\W]*?)\)(?:[\s\\]*?->[\s\\]*?([\w\(\)\[\]\,]+))?[\s\\]*?:)",
    flags=re.MULTILINE)
not_whitespace_pattern = re.compile(r"\S+", flags=re.MULTILINE)
arg_pattern = re.compile(r"([\w\*\/]+)(?:\s*?:\s*?([\w\[\]\(\)\,]+))?(?:\s*?=\s*?(.+))?")
class_pattern = re.compile(r"\s*class\s+?\w+\s*?(?:\((.*)\))?\s*?:")


def split_args(args: str) -> List[str]:
    from ..data_structures.stack import Stack

    res = []
    stack: Stack[str] = Stack()
    start = 0
    for i, char in enumerate(args):
        if char not in {'(', ')', '[', ']', ','}:
            continue
        if char in {'(', "["}:
            stack.push(char)
        elif char in {')', ']'}:
            stack.pop()
        elif stack.is_empty():
            res.append(args[start:i])
            start = i + 1

    res.append(args[start:len(args)])
    return res


def _format_type_name(type_obj: Any) -> Optional[str]:
    if type_obj is None or type_obj is inspect.Parameter.empty:
        return None
    origin = getattr(type_obj, "__origin__", None)
    if origin is not None:
        args = getattr(type_obj, "__args__", ())
        formatted_args = ", ".join(_format_type_name(arg) or str(arg) for arg in args)
        origin_name = getattr(origin, "__name__", str(origin).replace("typing.", ""))
        return f"{origin_name}[{formatted_args}]"
    if hasattr(type_obj, "__name__"):
        return type_obj.__name__
    return str(type_obj).replace("typing.", "")


def _extract_generics_from_cls(cls: type) -> List[str]:
    parameters: List[str] = []
    for param in getattr(cls, "__parameters__", ()):
        parameters.append(param.__name__)
    return parameters


def remove_whitespace(text: str) -> str:
    return "".join(not_whitespace_pattern.findall(text.strip())).replace("\\", "")


@dataclass(**function_declaration_kwargs)
class FunctionDeclaration:
    name: str
    arguments: Tuple[Argument, ...]
    return_type: Optional[str]
    decorators: Optional[List[str]] = None
    generics: Optional[Tuple[str, ...]] = None

    def duplicate(self, **override_kwargs) -> 'FunctionDeclaration':
        data = dict(
            name=self.name,
            arguments=self.arguments,
            return_type=self.return_type,
            decorators=self.decorators,
            generics=self.generics,
        )
        data.update(override_kwargs)
        return FunctionDeclaration(**data)

    @property
    def has_generics(self) -> bool:
        return self.generics is not None and len(self.generics) > 0

    @staticmethod
    def _from_runtime(cls: type) -> List['FunctionDeclaration']:
        parameters = _extract_generics_from_cls(cls)
        res: List[FunctionDeclaration] = []
        for name, obj in cls.__dict__.items():
            if not inspect.isfunction(obj):
                continue
            sig = inspect.signature(obj)
            arguments: List[Argument] = []
            for pname, param in sig.parameters.items():
                if pname == "self":
                    continue
                ptype = _format_type_name(
                    param.annotation if param.annotation is not inspect.Parameter.empty else None
                )
                default = None if param.default is inspect.Parameter.empty else repr(param.default)
                arguments.append(Argument(pname, ptype, default))
            return_type = _format_type_name(
                sig.return_annotation if sig.return_annotation is not inspect.Signature.empty else None
            )
            res.append(FunctionDeclaration(
                name,
                tuple(arguments),
                return_type,
                decorators=None,
                generics=tuple(parameters) or None,
            ))
        return res

    @staticmethod
    def get_declared_functions(cls) -> List['FunctionDeclaration']:
        if not isinstance(cls, type):
            raise TypeError('cls must be a Class')
        try:
            src = inspect.getsource(cls)
        except (OSError, TypeError):
            return FunctionDeclaration._from_runtime(cls)
        bases = [item for item in map(remove_whitespace, class_pattern.findall(src)) if len(item) > 0]
        parameters: List[str] = []
        for base in bases:
            if '[' in base and ']' in base:
                generic_args = base[base.index('[') + 1:base.rindex(']')]
                for arg in split_args(generic_args):
                    if len(arg) == 1:
                        parameters.append(arg)
        res = []
        for _, name, args, ret in func_pattern.findall(src):
            name = name.strip()
            args = remove_whitespace(args) if args is not None else None
            arguments = []
            if args is not None:
                for arg in split_args(args):
                    match = arg_pattern.match(remove_whitespace(arg))
                    if match is not None:
                        arguments.append(Argument(*match.groups()))
            return_type = ret.strip() if ret is not None and len(ret) != 0 else None
            res.append(FunctionDeclaration(
                name,
                tuple(arguments),
                return_type,
                decorators=None,
                generics=tuple(parameters) or None,
            ))
        return res

    def __eq__(self, other) -> bool:
        if not isinstance(other, FunctionDeclaration):
            return False
        return (
            self.name == other.name
            and self.arguments == other.arguments
            and self.return_type == other.return_type
        )

    def __hash__(self) -> int:
        return hash((self.name, self.arguments, self.return_type))


class _ProtocolMarker(Protocol):
    ...


_ProtocolMeta = type(_ProtocolMarker)
del _ProtocolMarker


@dataclass
class ClassDeclaration:
    cls: Type
    name: str
    module: str
    bases: Tuple[Type, ...]
    generics: Optional[Tuple[str, ...]]
    functions: List[FunctionDeclaration]

    @staticmethod
    def from_cls(cls) -> 'ClassDeclaration':
        if not isinstance(cls, type):
            raise TypeError('obj must be a Class')

        try:
            src = "\n".join(
                line for line in inspect.getsource(cls).splitlines()
                if not remove_whitespace(line).startswith("@")
            )
            match = class_pattern.match(src)
            bases = match.group(1).split(",") if match and match.group(1) else []
            parameters: List[str] = []
            for base in bases:
                if '[' in base and ']' in base:
                    generic_args = base[base.index('[') + 1:base.rindex(']')]
                    for arg in split_args(generic_args):
                        if len(arg) == 1:
                            parameters.append(arg)
        except (OSError, TypeError):
            parameters = _extract_generics_from_cls(cls)

        return ClassDeclaration(
            cls,
            cls.__name__,
            cls.__module__,
            getattr(cls, "__orig_bases__", getattr(cls, "__args__", ())),
            tuple(parameters) or None,
            FunctionDeclaration.get_declared_functions(cls),
        )

    @property
    def is_generic(self) -> bool:
        return self.generics is not None and len(self.generics) > 0


__all__ = [
    "Argument",
    "ClassDeclaration",
    "FunctionDeclaration",
    "get_explicitly_declared_functions",
    "get_mro",
]
