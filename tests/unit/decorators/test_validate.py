# type:ignore
import unittest
from typing import Any, Union
try:
    from danielutils import validate
    from danielutils.exceptions import EmptyAnnotationException, InvalidDefaultValueException, ValidationException, \
        InvalidReturnValueException
except:
    # python == 3.9.0
    from ...danielutils import validate
    from ...danielutils.exceptions import EmptyAnnotationException, InvalidDefaultValueException, ValidationException, \
        InvalidReturnValueException



class TestValidate(unittest.TestCase):

    def test_empty_annotation_exception(self):
        with self.assertRaises(EmptyAnnotationException):
            @validate
            def foo(x):
                pass

        with self.assertRaises(EmptyAnnotationException):
            @validate
            def foo1(x) -> Any:
                pass

        with self.assertRaises(EmptyAnnotationException):
            @validate
            def foo2(x, y: str):
                pass

        with self.assertRaises(EmptyAnnotationException):
            @validate
            def foo3(x, y: str, *args):
                pass

        @validate
        def foo4(*args):
            pass

        with self.assertRaises(EmptyAnnotationException):
            @validate
            def foo5(a: str, /, k=1):
                pass

    def test_invalid_default_value_exception(self):
        with self.assertRaises(InvalidDefaultValueException):
            @validate
            def foo(x: str = 1):
                pass

        @validate
        def foo2(x: int = 1):
            pass

    def test_validation_exception(self):
        @validate
        def foo(x: Union[int, str]):
            pass

        with self.assertRaises(ValidationException):
            foo(1.5)

        foo("aaa")

    def test_invalid_return_value_exception(self):
        @validate
        def foo() -> int:
            return 0.5

        with self.assertRaises(InvalidReturnValueException):
            foo()

        @validate
        def foo2() -> str:
            return "str"

        foo2()
