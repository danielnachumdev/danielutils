import logging
import inspect
import json
import re
from typing import List, Iterable, Type, TypeVar, Generic, get_origin
from .function_info import FunctionInfo
from .decorator_info import DecoratorInfo
from .argument_info import ArgumentInfo
from ...functions import isoftype
from ...logging_.utils import get_logger

logger = get_logger(__name__)

T = TypeVar("T")


class _A(Generic[T]):
    ...


_GenericAlias = type(_A[int])

del T, _A


class ClassInfo:
    CLASS_DEFINITION_REGEX: re.Pattern = re.compile(
        r"(?P<decorations>[\s\S]*)?(^)?class (?P<name>\w[\w\d]*)(?:\((?P<bases>.*)\))?:(?P<body>[\s\S]+)", re.MULTILINE)

    # r"(?P<decorations>[\s\S]*)?^class (?P<name>\w[\w\d]*)(?:\((?P<bases>.*)\))?:(?P<body>[\s\S]+)"

    def __init__(self, cls: Type) -> None:
        logger.debug(f"Creating ClassInfo for: {cls}")
        if isoftype(cls, _GenericAlias):  # type:ignore
            logger.debug("Converting generic alias to origin type")
            cls = get_origin(cls)  # type:ignore
        if not inspect.isclass(cls):
            error_msg = f"'{cls.__name__}' is not a class"
            logger.error(f"ClassInfo creation failed: {error_msg}")
            raise TypeError(error_msg)
        self._cls = cls
        self._src_code: str = ""
        self._name: str = ""
        self._bases: List[ArgumentInfo] = []
        self._functions: List[FunctionInfo] = []
        self._decorations: List[DecoratorInfo] = []
        logger.debug(f"Parsing source code for class: {cls.__name__}")
        self._parse_src_code()
        logger.info(f"ClassInfo created successfully for: {cls.__name__}")

    def _parse_src_code(self) -> None:
        logger.debug("Parsing source code")
        self._src_code = inspect.getsource(self._cls)
        m = ClassInfo.CLASS_DEFINITION_REGEX.match(self._src_code)
        if m is None:
            logger.error("Failed to match class definition regex")
            raise SyntaxError()
        decorators, name, bases, _ = m.groupdict().values()
        logger.debug(f"Parsed class name: {name}, bases: {bases}")
        self._name = name
        self._bases = ArgumentInfo.from_str(bases)
        logger.debug(f"Parsed {len(self._bases)} base classes")
        self._parse_body()

        if decorators is not None:
            logger.debug(f"Parsing {len(decorators.strip().splitlines())} decorators")
            for substr in decorators.strip().splitlines():
                self._decorations.append(
                    DecoratorInfo.from_str(substr.strip()))
        logger.debug(f"Parsed {len(self._decorations)} decorators")

    def _parse_body(self) -> None:
        for attr in dir(self._cls):
            obj = getattr(self._cls, attr, None)
            if inspect.isbuiltin(obj):
                continue
            try:
                if inspect.isroutine(obj):
                    inspect.getsource(obj)
                elif inspect.isdatadescriptor(obj):
                    inspect.getsource(obj.fget)  # type:ignore
                else:
                    continue
            except:
                continue

            try:
                self._functions.append(FunctionInfo(
                    obj, self._cls))  # type: ignore
            except Exception as e:
                raise Exception(
                    f"Error parsing function '{attr}' of class '{self._name}': {e}", e) from e

    def __str__(self) -> str:
        body = json.dumps({
            "name": self.name,
            "bases": self.bases,
            "decorations": self.decorations,
            "static_methods": self.static_methods,
            "class_methods": self.class_methods,
            "instance_methods": self.instance_methods
        }, default=str, indent=4)[1:-1]
        return f"{self.__class__.__name__}({body})"

    def __repr__(self):
        return f"{self.__class__.__name__}(name=\"{self.name}\")"

    @property
    def name(self) -> str:
        return self._name

    @property
    def decorations(self) -> List[DecoratorInfo]:
        return self._decorations

    @property
    def bases(self) -> List[ArgumentInfo]:
        return self._bases

    @property
    def static_methods(self) -> Iterable[FunctionInfo]:
        return sorted(filter(lambda f: f.is_static_method, self._functions), key=lambda f: f.name)

    @property
    def class_methods(self) -> Iterable[FunctionInfo]:
        return sorted(filter(lambda f: f.is_class_method, self._functions), key=lambda f: f.name)

    @property
    def instance_methods(self) -> Iterable[FunctionInfo]:
        return sorted(filter(lambda f: f.is_instance_method, self._functions), key=lambda f: f.name)

    @property
    def inherited_methods(self) -> Iterable[FunctionInfo]:
        return sorted(filter(lambda f: f.is_inherited, self._functions), key=lambda f: f.name)

    @property
    def abstract_methods(self) -> Iterable[FunctionInfo]:
        return sorted(filter(lambda f: f.is_abstract, self._functions), key=lambda f: f.name)

    @property
    def functions(self) -> List[FunctionInfo]:
        return self._functions

    @property
    def properties(self):
        pass

    @property
    def instance_properties(self):
        pass

    @property
    def class_properties(self):
        pass


__all__ = [
    "ClassInfo"
]
