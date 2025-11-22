import unittest

from danielutils.reflection.info_classes.class_info import ClassInfo
from danielutils.reflection.info_classes.function_info import FunctionInfo
from danielutils.reflection.info_classes.decorator_info import DecoratorInfo


class TestDecoratorParsing(unittest.TestCase):
    """Test cases for decorator parsing in classes and functions."""

    def test_class_decorator_no_parameters(self):
        """Test class with decorator that has no parameters."""

        def simple_decorator(cls):
            return cls

        @simple_decorator
        class TestClass:
            def method(self):
                pass

        class_info = ClassInfo(TestClass)
        self.assertEqual(1, len(class_info.decorations))
        self.assertEqual("simple_decorator", class_info.decorations[0].name)
        self.assertEqual(0, len(class_info.decorations[0].arguments))

    def test_class_decorator_positional_parameters(self):
        """Test class with decorator that has positional parameters."""

        def decorator_with_args(*args, **kwargs):
            def decorator(cls):
                return cls

            return decorator

        @decorator_with_args(1, 2, 3)
        class TestClass:
            def method(self):
                pass

        class_info = ClassInfo(TestClass)
        self.assertEqual(1, len(class_info.decorations))
        self.assertEqual("decorator_with_args", class_info.decorations[0].name)
        self.assertEqual(3, len(class_info.decorations[0].arguments))

    def test_class_decorator_keyword_parameters(self):
        """Test class with decorator that has keyword parameters."""

        def decorator_with_kwargs(*args, **kwargs):
            def decorator(cls):
                return cls

            return decorator

        @decorator_with_kwargs(a=1, b=2)
        class TestClass:
            def method(self):
                pass

        class_info = ClassInfo(TestClass)
        self.assertEqual(1, len(class_info.decorations))
        self.assertEqual("decorator_with_kwargs",
                         class_info.decorations[0].name)
        self.assertEqual(2, len(class_info.decorations[0].arguments))
        # Check that arguments have names (keyword arguments)
        arg_names = [arg.name for arg in class_info.decorations[0].arguments]
        self.assertIn("a", arg_names)
        self.assertIn("b", arg_names)

    def test_class_decorator_mixed_parameters(self):
        """Test class with decorator that has both positional and keyword parameters."""

        def decorator_mixed(*args, **kwargs):
            def decorator(cls):
                return cls

            return decorator

        @decorator_mixed(1, 2, a=3, b=4)
        class TestClass:
            def method(self):
                pass

        class_info = ClassInfo(TestClass)
        self.assertEqual(1, len(class_info.decorations))
        self.assertEqual("decorator_mixed", class_info.decorations[0].name)
        self.assertEqual(4, len(class_info.decorations[0].arguments))
        # Check that some arguments have names (keyword) and some don't (positional)
        arg_names = [arg.name for arg in class_info.decorations[0].arguments]
        # Positional arguments might not have names, keyword arguments should
        has_keyword_args = any(name is not None and name in [
            "a", "b"] for name in arg_names)
        self.assertTrue(has_keyword_args)

    def test_function_decorator_no_parameters(self):
        """Test function in class with decorator that has no parameters."""

        def simple_decorator(func):
            return func

        class TestClass:
            @simple_decorator
            def method(self):
                pass

        func_info = FunctionInfo(TestClass.method, TestClass)
        self.assertEqual(1, len(func_info.decorators))
        self.assertEqual("simple_decorator", func_info.decorators[0].name)
        self.assertEqual(0, len(func_info.decorators[0].arguments))

    def test_function_decorator_positional_parameters(self):
        """Test function in class with decorator that has positional parameters."""

        def decorator_with_args(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        class TestClass:
            @decorator_with_args(1, 2, 3)
            def method(self):
                pass

        func_info = FunctionInfo(TestClass.method, TestClass)
        self.assertEqual(1, len(func_info.decorators))
        self.assertEqual("decorator_with_args", func_info.decorators[0].name)
        self.assertEqual(3, len(func_info.decorators[0].arguments))

    def test_function_decorator_keyword_parameters(self):
        """Test function in class with decorator that has keyword parameters."""

        def decorator_with_kwargs(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        class TestClass:
            @decorator_with_kwargs(a=1, b=2)
            def method(self):
                pass

        func_info = FunctionInfo(TestClass.method, TestClass)
        self.assertEqual(1, len(func_info.decorators))
        self.assertEqual("decorator_with_kwargs", func_info.decorators[0].name)
        self.assertEqual(2, len(func_info.decorators[0].arguments))
        # Check that arguments have names (keyword arguments)
        arg_names = [arg.name for arg in func_info.decorators[0].arguments]
        self.assertIn("a", arg_names)
        self.assertIn("b", arg_names)

    def test_function_decorator_mixed_parameters(self):
        """Test function in class with decorator that has both positional and keyword parameters."""

        def decorator_mixed(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        class TestClass:
            @decorator_mixed(1, 2, a=3, b=4)
            def method(self):
                pass

        func_info = FunctionInfo(TestClass.method, TestClass)
        self.assertEqual(1, len(func_info.decorators))
        self.assertEqual("decorator_mixed", func_info.decorators[0].name)
        self.assertEqual(4, len(func_info.decorators[0].arguments))
        # Check that some arguments have names (keyword) and some don't (positional)
        arg_names = [arg.name for arg in func_info.decorators[0].arguments]
        # Positional arguments might not have names, keyword arguments should
        has_keyword_args = any(name is not None and name in [
            "a", "b"] for name in arg_names)
        self.assertTrue(has_keyword_args)

    def test_function_decorator_string_parameter(self):
        """Test function in class with decorator that has one string parameter."""

        def decorator_with_string(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        class TestClass:
            @decorator_with_string("test_string")
            def method(self):
                pass

        func_info = FunctionInfo(TestClass.method, TestClass)
        self.assertEqual(1, len(func_info.decorators))
        self.assertEqual("decorator_with_string", func_info.decorators[0].name)
        self.assertEqual(1, len(func_info.decorators[0].arguments))
        # Check that the argument value is a string
        arg = func_info.decorators[0].arguments[0]
        # The default value should contain the string (might be quoted)
        self.assertIsNotNone(arg.default)
        self.assertIn("test_string", arg.default)

    def test_class_decorator_string_parameter(self):
        """Test class with decorator that has one string parameter."""

        def decorator_with_string(*args, **kwargs):
            def decorator(cls):
                return cls

            return decorator

        @decorator_with_string("test_string")
        class TestClass:
            def method(self):
                pass

        class_info = ClassInfo(TestClass)
        self.assertEqual(1, len(class_info.decorations))
        self.assertEqual("decorator_with_string",
                         class_info.decorations[0].name)
        self.assertEqual(1, len(class_info.decorations[0].arguments))
        # Check that the argument value is a string
        arg = class_info.decorations[0].arguments[0]
        # The default value should contain the string (might be quoted)
        self.assertIsNotNone(arg.default)
        self.assertIn("test_string", arg.default)

    def test_multiple_decorators_on_class(self):
        """Test class with multiple decorators of different types."""

        def decorator1(cls):
            return cls

        def decorator2(*args, **kwargs):
            def decorator(cls):
                return cls

            return decorator

        @decorator1
        @decorator2(1, 2)
        class TestClass:
            def method(self):
                pass

        class_info = ClassInfo(TestClass)
        self.assertEqual(2, len(class_info.decorations))
        decorator_names = [d.name for d in class_info.decorations]
        self.assertIn("decorator1", decorator_names)
        self.assertIn("decorator2", decorator_names)

    def test_multiple_decorators_on_function(self):
        """Test function in class with multiple decorators of different types."""

        def decorator1(func):
            return func

        def decorator2(*args, **kwargs):
            def decorator(func):
                return func

            return decorator

        class TestClass:
            @decorator1
            @decorator2("test")
            def method(self):
                pass

        func_info = FunctionInfo(TestClass.method, TestClass)
        self.assertEqual(2, len(func_info.decorators))
        decorator_names = [d.name for d in func_info.decorators]
        self.assertIn("decorator1", decorator_names)
        self.assertIn("decorator2", decorator_names)

    def test_decorator_info_from_str_with_string_parameter(self):
        """Test DecoratorInfo.from_str directly with string parameter."""
        # This should not raise an exception
        decorator_info = DecoratorInfo.from_str('@decorator_with_string("test_string")')

        self.assertEqual("decorator_with_string", decorator_info.name)
        self.assertEqual(1, len(decorator_info.arguments))
        # Check that the argument value contains the string
        arg = decorator_info.arguments[0]
        self.assertIsNotNone(arg.default)
        self.assertIn("test_string", arg.default)


if __name__ == '__main__':
    unittest.main()
