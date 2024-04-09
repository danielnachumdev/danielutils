import unittest
from danielutils.reflection import *


class TestFunctionReflections(unittest.TestCase):
    def test_get_caller_name(self) -> None:
        self.assertEqual('test_get_caller_name', get_caller_name(0))

        def bar() -> None:
            self.assertEqual('bar', get_caller_name(0))
            self.assertEqual('foo', get_caller_name(1))
            self.assertEqual('test_get_caller_name', get_caller_name(2))

        def foo() -> None:
            bar()

        foo()

    def test_get_function_return_type(self):
        def foo(): ...

        self.assertEqual(type(None), get_function_return_type(foo))

        def foo() -> None: ...

        self.assertEqual(type(None), get_function_return_type(foo))

        def foo() -> int: ...

        self.assertEqual(int, get_function_return_type(foo))

    def test_is_function_annotated_properly(self):
        def foo1(): ...

        self.assertTrue(is_function_annotated_properly(foo1))

        def foo2() -> None: ...

        self.assertTrue(is_function_annotated_properly(foo2))

        def foo3() -> int: ...

        self.assertTrue(is_function_annotated_properly(foo3))

    def test_get_current_func(self):
        self.assertEqual(self.test_get_current_func, get_current_func())
