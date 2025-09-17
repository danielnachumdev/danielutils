import inspect, re
import logging
from typing import Any, List as List, Optional, Tuple as Tuple, Type, Protocol
from dataclasses import dataclass
from ..interpreter import get_python_version
from ...logging_.utils import get_logger

logger = get_logger(__name__)

argument_kwargs = dict(frozen=True)
FunctionDeclaration_kwargs = dict(frozen=True)
if get_python_version() >= (3, 9):
    from builtins import list as List, tuple as Tuple  # type:ignore

elif get_python_version() >= (3, 10):
    argument_kwargs.update(slots=True)
    FunctionDeclaration_kwargs.update(slots=True)


def get_explicitly_declared_functions(cls: type) -> List[str]:
    """
    Returns the names of the functions that are explicitly declared in a class.

    This function does not return inherited functions.

    Args:
        cls (type): The class to inspect.

    Returns:
        list[str]: A list of names of the functions explicitly declared in the class.
    """
    functions = [func for func, val in inspect.getmembers(cls, predicate=inspect.isfunction)]
    return functions


def get_mro(obj: Any) -> List[type]:
    """returns the mro of an object

    Args:
        obj (Any): any object, instance or class

    Returns:
        list[type]: the resulting mro for the object
    """
    if isinstance(obj, type):
        mro = obj.mro()
        return mro
    return get_mro(obj.__class__)


@dataclass(**argument_kwargs)
class Argument:
    name: str
    type: Optional[str]
    default: Optional[str]

    def __hash__(self) -> int:
        t = self.type
        if self.type is not None and "Union" in self.type:
            t = set(self.type[self.type.index("[") + 1:self.type.rindex("]")].split(","))
            t = tuple(sorted(t))
        return hash((self.name, t, self.default))

    def duplicate(self, **override_kwargs) -> 'Argument':
        dct = dict(
            name=self.name,
            type=self.type,
            default=self.default,
        )
        dct.update(override_kwargs)
        result = Argument(**dct)
        return result


func_pattern = re.compile(
    r"(.*def[\s\\]*?(\w+)[\s\\]*?\(([\w\W]*?)\)(?:[\s\\]*?->[\s\\]*?([\w\(\)\[\]\,]+))?[\s\\]*?:)",
    flags=re.MULTILINE)
not_whitespace_pattern = re.compile(r"\S+", flags=re.MULTILINE)
arg_pattern = re.compile(r"([\w\*\/]+)(?:\s*?:\s*?([\w\[\]\(\)\,]+))?(?:\s*?=\s*?(.+))?")
class_pattern = re.compile(r"\s*class\s+?\w+\s*?(?:\((.*)\))?\s*?:")


def split_args(args: str) -> List[str]:
    from danielutils import Stack
    res = []
    s: Stack[str] = Stack()
    start = 0
    for i, c in enumerate(args):
        if c not in {'(', ')', '[', ']', ','}:
            continue
        if c in {'(', "["}:
            s.push(c)
        elif c in {')', ']'}:
            s.pop()
        else:
            if s.is_empty():
                res.append(args[start:i])
                start = i + 1

    res.append(args[start:len(args)])
    return res


def remove_whitespace(text: str) -> str:
    return "".join(not_whitespace_pattern.findall(text.strip())).replace("\\", "")


@dataclass(**FunctionDeclaration_kwargs)
class FunctionDeclaration:
    name: str
    arguments: Tuple[Argument, ...]
    return_type: Optional[str]
    decorators: Optional[List[str]] = None
    generics: Optional[Tuple[str]] = None

    def duplicate(self, **override_kwargs) -> 'FunctionDeclaration':
        dct = dict(
            name=self.name,
            arguments=self.arguments,
            return_type=self.return_type,
            decorators=self.decorators,
            generics=self.generics,
        )
        dct.update(override_kwargs)
        result = FunctionDeclaration(**dct)  # type:ignore
        return result

    @property
    def has_generics(self) -> bool:
        has_generics = self.generics is not None and len(self.generics) > 0
        return has_generics

    @staticmethod
    def get_declared_functions(cls) -> List['FunctionDeclaration']:
        """will yield the names of all the functions declared inside a class

        Yields:
            Generator[str, None, None]: yields str values which are names of declared functions
        """
        if not isinstance(cls, type):
            logger.error(f"Invalid type for cls: {type(cls)}, expected type")
            raise TypeError('cls must be a Class')
        
        src = inspect.getsource(cls)
        
        bases = [o for o in map(remove_whitespace, class_pattern.findall(src)) if len(o) > 0]
        
        parameters = []
        for base in bases:
            if '[' in base and ']' in base:
                s = base[base.index('[') + 1:base.rindex(']')]
                for arg in split_args(s):
                    if len(arg) == 1:
                        parameters.append(arg)
        
        res = []
        function_matches = func_pattern.findall(src)
        
        for code, name, args, ret in function_matches:
            name: str = name.strip()  # type:ignore
            args: Optional[str] = remove_whitespace(args) if args is not None else None  # type:ignore
            arguments = []
            if args is not None:
                for arg in split_args(args):
                    arguments.append(Argument(*arg_pattern.match(remove_whitespace(arg)).groups()))
            ret: Optional[str] = ret.strip() if ret is not None and len(ret) != 0 else None # type:ignore
            func_decl = FunctionDeclaration(name, tuple(arguments), ret, decorators=None, generics=tuple(parameters))
            res.append(func_decl)

        return res

    def __eq__(self, other) -> bool:
        if not isinstance(other, FunctionDeclaration):
            return False

        result = self.name == other.name and self.arguments == other.arguments and self.return_type == other.return_type
        return result

    def __hash__(self) -> int:
        return hash((self.name, self.arguments, self.return_type))

    def __str__(self) -> str:
        args = ",\n\t\t".join(map(str, self.arguments))
        return f"{self.__class__.__name__}(\n" \
               f"\tname='{self.name}',\n" \
               f"\targuments=(\n" \
               f"\t\t{args}\n" \
               f"\t),\n" \
               f"\treturn_type={self.return_type},\n" \
               f"\tdecorators={self.decorators}\n" \
               f")"


class _tmp(Protocol): ...


_ProtocolMeta = type(_tmp)
del _tmp


@dataclass
class ClassDeclaration:
    cls: Type
    name: str
    module: str
    bases: Tuple[Type]
    generics: Optional[Tuple[str]]
    functions: List[FunctionDeclaration]

    @staticmethod
    def from_cls(cls) -> 'ClassDeclaration':
        if type(cls) not in {type, _ProtocolMeta}:
            logger.error(f"Invalid type for cls: {type(cls)}, expected type or Protocol")
            raise TypeError('obj must be a Class')

        src = "\n".join([l for l in inspect.getsource(cls).splitlines() if not remove_whitespace(l).startswith("@")])
        
        bases = class_pattern.match(src).group(1).split(",")
        
        parameters = []
        for base in bases:
            if '[' in base and ']' in base:
                s = base[base.index('[') + 1:base.rindex(']')]
                for arg in split_args(s):
                    if len(arg) == 1:
                        parameters.append(arg)

        orig_bases = getattr(cls, "__orig_bases__", getattr(cls, "__args__", ()))
        functions = FunctionDeclaration.get_declared_functions(cls)
        
        result = ClassDeclaration(
            cls,
            cls.__name__,
            cls.__module__,
            orig_bases,
            tuple(parameters) or None,
            functions
        )
        return result

    @property
    def is_generic(self) -> bool:
        is_generic = self.generics is not None and len(self.generics) > 0
        return is_generic


__all__ = [
    "get_explicitly_declared_functions",
    "get_mro",
    "FunctionDeclaration",
    "ClassDeclaration"
]
