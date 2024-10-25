import inspect
import re
from typing import Optional, List, Iterable, Type, TypeVar, Generic, get_origin
from .function_info import FunctionInfo
from .decoration_info import DecorationInfo
from .argument_info import ArgumentInfo
from danielutils.functions import isoftype

T = TypeVar("T")


class _A(Generic[T]): ...


_GenericAlias = type(_A[int])

del T, _A


class ClassInfo:
    CLASS_DEFINITION_REGEX: re.Pattern = re.compile(
        r"(?P<decorations>[\s\S]*)?^class (?P<name>\w[\w\d]*)(?:\((?P<bases>.*)\))?:(?P<body>[\s\S]+)", re.MULTILINE)

    # r"(?P<decorations>[\s\S]*)?^class (?P<name>\w[\w\d]*)(?:\((?P<bases>.*)\))?:(?P<body>[\s\S]+)"

    def __init__(self, cls: Type) -> None:
        if isoftype(cls, _GenericAlias):  # type:ignore
            cls = get_origin(cls)  # type:ignore
        if not inspect.isclass(cls):
            raise TypeError(f"'{cls.__name__}' is not a class")
        self._cls = cls
        self._src_code: str = ""
        self._name: str = ""
        self._bases: List[ArgumentInfo] = []
        self._functions: List[FunctionInfo] = []
        self._decorations: List[DecorationInfo] = []
        self._parse_src_code()

    def _parse_src_code(self) -> None:
        self._src_code = inspect.getsource(self._cls)
        m = ClassInfo.CLASS_DEFINITION_REGEX.match(self._src_code)
        if m is None:
            raise SyntaxError()
        decorators, name, bases, _ = m.groups()
        self._name = name
        self._bases = ArgumentInfo.from_str(bases)
        self._parse_body()

        if decorators is not None:
            for substr in decorators.strip().splitlines():
                self._decorations.append(DecorationInfo.from_str(substr.strip()))

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
                    raise Exception()
            except:
                continue
            self._functions.append(FunctionInfo(obj, self._cls))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(name=\"{self.name}\", bases={self.bases}, decorations={self.decorations}, static_methods={self.static_methods}, class_methods={self.class_methods}, isntance_methods={self.instance_methods})"

    def __repr__(self):
        return f"{self.__class__.__name__}(name=\"{self.name}\")"

    @property
    def name(self) -> str:
        return self._name

    @property
    def decorations(self) -> List[DecorationInfo]:
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
    def inherited_methods(self)->Iterable[FunctionInfo]:
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
