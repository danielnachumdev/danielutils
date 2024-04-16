import inspect, re
from typing import Any, List as t_list, Optional
from .interpreter import get_python_version

if get_python_version() >= (3, 9):
    from builtins import list as t_list  # type:ignore


def get_explicitly_declared_functions(cls: type) -> t_list[str]:
    """
    Returns the names of the functions that are explicitly declared in a class.

    This function does not return inherited functions.

    Args:
        cls (type): The class to inspect.

    Returns:
        list[str]: A list of names of the functions explicitly declared in the class.
    """
    return [func for func, val in inspect.getmembers(cls, predicate=inspect.isfunction)]


def get_mro(obj: Any) -> t_list[type]:
    """returns the mro of an object

    Args:
        obj (Any): any object, instance or class

    Returns:
        list[type]: the resulting mro for the object
    """
    if isinstance(obj, type):
        return obj.mro()
    return get_mro(obj.__class__)


from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Argument:
    name: str
    type: Optional[str]
    default: Optional[str]


@dataclass(frozen=True, slots=True)
class FunctionDeclaration:
    name: str
    arguments: tuple[Argument, ...]
    return_type: str
    decorators: Optional[list[str]] = None

    @staticmethod
    def get_declared_functions(cls) -> list['FunctionDeclaration']:
        """will yield the names of all the functions declared inside a class

        Yields:
            Generator[str, None, None]: yields str values which are names of declared functions
        """
        if not isinstance(cls, type):
            raise TypeError('cls must be a Class')
        from danielutils import Stack
        def split_args(args: str) -> list[str]:
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

        func_pattern = re.compile(
            r"(.*def[\s\\]*?(\w+)[\s\\]*?\(([\w\W]*?)\)(?:[\s\\]*?->[\s\\]*?([\w\(\)\[\]\,]+))?[\s\\]*?:)",
            flags=re.MULTILINE)
        not_whitespace_pattern = re.compile(r"\S+", flags=re.MULTILINE)
        arg_pattern = re.compile(r"([\w\*\/]+)(?:\s*?:\s*?([\w\[\]\(\)\,]+))?(?:\s*?=\s*?(.+))?")
        src = inspect.getsource(cls)
        res = []
        for code, name, args, ret in func_pattern.findall(src):
            name: str = name.strip()
            args: Optional[str] = \
                "".join(not_whitespace_pattern.findall(args.strip())).replace("\\", "") \
                    if args is not None else \
                    None
            arguments = []
            if args is not None:
                for arg in split_args(args):
                    arguments.append(Argument(*arg_pattern.match(arg).groups()))
            ret: Optional[str] = ret.strip() if ret is not None else None
            res.append(FunctionDeclaration(name, tuple(arguments), ret))
        return res


__all__ = [
    "get_explicitly_declared_functions",
    "get_mro",
    "FunctionDeclaration"
]
