import pytest
from ...danielutils import validate
from ...danielutils.Exceptions import *
from typing import Any, Union


def test_empty_annotation_exception():
    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo(x):
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo(x) -> Any:
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo(x, y: str):
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo(x, y: str, *args):
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo(*args):
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo(a: str, /, k=1):
            pass


def test_invalid_default_value_exception():

    with pytest.raises(InvalidDefaultValueException):
        @validate
        def foo(x: str = 1):
            pass

    @validate
    def foo(x: int = 1):
        pass


def test_validation_exception():
    @validate
    def foo(x: Union[int, str]):
        pass
    with pytest.raises(ValidationException):
        foo(1.5)

    foo("aaa")


def test_invalid_return_value_exception():
    @validate
    def foo() -> int:
        return 0.5
    with pytest.raises(InvalidReturnValueException):
        foo()

    @validate
    def foo() -> str:
        return "str"

    foo()
