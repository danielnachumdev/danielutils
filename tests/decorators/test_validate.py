# type:ignore
from typing import Any, Union
import pytest
from ...danielutils import validate
from ...danielutils.exceptions import EmptyAnnotationException, InvalidDefaultValueException, ValidationException, InvalidReturnValueException


def test_empty_annotation_exception():
    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo(x):
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo1(x) -> Any:
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo2(x, y: str):
            pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo3(x, y: str, *args):
            pass

    @validate
    def foo4(*args):
        pass

    with pytest.raises(EmptyAnnotationException):
        @validate
        def foo5(a: str, /, k=1):
            pass


def test_invalid_default_value_exception():

    with pytest.raises(InvalidDefaultValueException):
        @validate
        def foo(x: str = 1):
            pass

    @validate
    def foo2(x: int = 1):
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
    def foo2() -> str:
        return "str"

    foo2()
