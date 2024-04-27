import unittest

try:
    from danielutils.reflection import *
except:
    # python == 3.9.0
    from ...danielutils.reflection import *


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
        def foo1(): ...

        self.assertEqual(type(None), get_function_return_type(foo1))

        def foo2() -> None: ...

        self.assertEqual(type(None), get_function_return_type(foo2))

        def foo3() -> int: ...  # type:ignore

        self.assertEqual(int, get_function_return_type(foo3))

    def test_is_function_annotated_properly(self):
        def foo1(): ...

        self.assertTrue(is_function_annotated_properly(foo1))

        def foo2() -> None: ...

        self.assertTrue(is_function_annotated_properly(foo2))

        def foo3() -> int: ...  # type:ignore

        self.assertTrue(is_function_annotated_properly(foo3))

        def foo4(x): ...

        self.assertFalse(is_function_annotated_properly(foo4))

        def foo5(x: int): ...

        self.assertTrue(is_function_annotated_properly(foo5))

        def foo6(x: int) -> None: ...

        self.assertTrue(is_function_annotated_properly(foo5))

    def test_get_current_func(self):
        self.assertEqual(self.test_get_current_func, get_current_func())
