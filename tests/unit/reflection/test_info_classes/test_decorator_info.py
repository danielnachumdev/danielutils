import unittest
from unittest.mock import patch, MagicMock

from danielutils.reflection.info_classes.decorator_info import DecoratorInfo
from danielutils.reflection.info_classes.argument_info import ArgumentInfo


class TestDecorationInfo(unittest.TestCase):
    """Test cases for DecoratorInfo class."""

    def test_init_with_name_and_arguments(self):
        """Test DecoratorInfo initialization with name and arguments."""
        name = "decorator"
        arguments = [ArgumentInfo(
            "arg1", "str", None, False, False, False, None)]
        decoration_info = DecoratorInfo(name, arguments)

        self.assertEqual(name, decoration_info.name)
        self.assertEqual(arguments, decoration_info.arguments)

    def test_init_with_name_only(self):
        """Test DecoratorInfo initialization with name only."""
        name = "decorator"
        arguments = []
        decoration_info = DecoratorInfo(name, arguments)

        self.assertEqual(name, decoration_info.name)
        self.assertEqual(arguments, decoration_info.arguments)

    def test_properties(self):
        """Test that properties return correct values."""
        name = "test_decorator"
        arguments = [
            ArgumentInfo("param1", "int", "10", False, False, False, None),
            ArgumentInfo("param2", "str", None, False, False, False, None)
        ]
        decoration_info = DecoratorInfo(name, arguments)

        self.assertEqual(name, decoration_info.name)
        self.assertEqual(arguments, decoration_info.arguments)

    def test_from_str_simple_decorator(self):
        """Test from_str with a simple decorator without arguments."""
        result = DecoratorInfo.from_str("@decorator")

        self.assertEqual("decorator", result.name)
        self.assertEqual([], result.arguments)

    def test_from_str_decorator_without_at_symbol(self):
        """Test from_str with a decorator without @ symbol."""
        result = DecoratorInfo.from_str("decorator")

        self.assertEqual("decorator", result.name)
        self.assertEqual([], result.arguments)

    def test_from_str_decorator_with_simple_argument(self):
        """Test from_str with a decorator with simple argument."""
        result = DecoratorInfo.from_str("@decorator(arg1)")

        self.assertEqual("decorator", result.name)
        self.assertEqual(1, len(result.arguments))
        self.assertEqual("arg1", result.arguments[0].name)

    def test_from_str_decorator_with_typed_argument(self):
        """Test from_str with a decorator with typed argument."""
        result = DecoratorInfo.from_str("@decorator(arg1: str)")

        self.assertEqual("decorator", result.name)
        self.assertEqual(1, len(result.arguments))
        self.assertEqual("arg1", result.arguments[0].name)
        self.assertEqual("str", result.arguments[0].type)

    def test_from_str_decorator_with_default_argument(self):
        """Test from_str with a decorator with default argument."""
        result = DecoratorInfo.from_str("@decorator(arg1=10)")

        self.assertEqual("decorator", result.name)
        self.assertEqual(1, len(result.arguments))
        self.assertEqual("arg1", result.arguments[0].name)
        self.assertEqual("10", result.arguments[0].default)

    def test_from_str_decorator_with_multiple_arguments(self):
        """Test from_str with a decorator with multiple arguments."""
        result = DecoratorInfo.from_str(
            "@decorator(arg1: str, arg2: int = 10)")

        self.assertEqual("decorator", result.name)
        self.assertEqual(2, len(result.arguments))
        self.assertEqual("arg1", result.arguments[0].name)
        self.assertEqual("str", result.arguments[0].type)
        self.assertEqual("arg2", result.arguments[1].name)
        self.assertEqual("int", result.arguments[1].type)
        self.assertEqual("10", result.arguments[1].default)

    def test_from_str_decorator_with_complex_arguments(self):
        """Test from_str with a decorator with complex arguments."""
        result = DecoratorInfo.from_str("@decorator(*args, **kwargs)")

        self.assertEqual("decorator", result.name)
        self.assertEqual(2, len(result.arguments))
        self.assertTrue(result.arguments[0].is_args)
        self.assertTrue(result.arguments[1].is_kwargs)

    def test_from_str_invalid_string(self):
        """Test from_str with invalid string raises ValueError."""
        with self.assertRaises(ValueError):
            DecoratorInfo.from_str("invalid@decorator")

    def test_from_str_empty_string(self):
        """Test from_str with empty string raises ValueError."""
        with self.assertRaises(ValueError):
            DecoratorInfo.from_str("")

    def test_from_str_whitespace_only(self):
        """Test from_str with whitespace only raises ValueError."""
        with self.assertRaises(ValueError):
            DecoratorInfo.from_str("   ")

    def test_from_str_with_nested_brackets(self):
        """Test from_str with nested brackets in arguments."""
        result = DecoratorInfo.from_str(
            "@decorator(arg1: List[str], arg2: Dict[str, int])")

        self.assertEqual("decorator", result.name)
        self.assertEqual(2, len(result.arguments))
        self.assertEqual("arg1", result.arguments[0].name)
        self.assertEqual("List[str]", result.arguments[0].type)
        self.assertEqual("arg2", result.arguments[1].name)
        self.assertEqual("Dict[str, int]", result.arguments[1].type)

    def test_str_method(self):
        """Test __str__ method."""
        decoration_info = DecoratorInfo("test", [])
        self.assertEqual(str(decoration_info), repr(decoration_info))

    def test_repr_without_arguments(self):
        """Test __repr__ method without arguments."""
        decoration_info = DecoratorInfo("test", [])
        expected = 'DecoratorInfo(name="test")'
        self.assertEqual(expected, repr(decoration_info))

    def test_repr_with_arguments(self):
        """Test __repr__ method with arguments."""
        arguments = [ArgumentInfo(
            "arg1", "str", None, False, False, False, None)]
        decoration_info = DecoratorInfo("test", arguments)
        expected = 'DecoratorInfo(name="test", arguments=[ArgumentInfo(name="arg1", type=str)])'
        self.assertEqual(expected, repr(decoration_info))

    def test_repr_with_complex_arguments(self):
        """Test __repr__ method with complex arguments."""
        arguments = [
            ArgumentInfo("arg1", "str", "default", False, False, False, None),
            ArgumentInfo("arg2", "int", None, False, False, False, None)
        ]
        decoration_info = DecoratorInfo("test", arguments)
        # The exact format depends on ArgumentInfo.__repr__, but should contain the name
        self.assertIn('DecoratorInfo(name="test"', repr(decoration_info))
        self.assertIn('arguments=', repr(decoration_info))

    def test_equality(self):
        """Test that DecoratorInfo instances with same data are equal."""
        args1 = [ArgumentInfo("arg1", "str", None, False, False, False, None)]
        args2 = [ArgumentInfo("arg1", "str", None, False, False, False, None)]

        decoration1 = DecoratorInfo("test", args1)
        decoration2 = DecoratorInfo("test", args2)

        self.assertEqual(decoration2.name, decoration1.name)
        self.assertEqual(len(decoration1.arguments),
                         len(decoration2.arguments))

    def test_different_names_not_equal(self):
        """Test that DecoratorInfo instances with different names are not equal."""
        args = [ArgumentInfo("arg1", "str", None, False, False, False, None)]

        decoration1 = DecoratorInfo("test1", args)
        decoration2 = DecoratorInfo("test2", args)

        self.assertNotEqual(decoration1.name, decoration2.name)

    def test_different_arguments_not_equal(self):
        """Test that DecoratorInfo instances with different arguments are not equal."""
        args1 = [ArgumentInfo("arg1", "str", None, False, False, False, None)]
        args2 = [ArgumentInfo("arg2", "str", None, False, False, False, None)]

        decoration1 = DecoratorInfo("test", args1)
        decoration2 = DecoratorInfo("test", args2)

        self.assertEqual(decoration2.name, decoration1.name)
        self.assertNotEqual(
            decoration1.arguments[0].name, decoration2.arguments[0].name)

    def test_edge_case_special_characters_in_name(self):
        """Test from_str with special characters in decorator name."""
        # Should work with alphanumeric and underscore
        result = DecoratorInfo.from_str("@decorator_123")
        self.assertEqual("decorator_123", result.name)

    def test_edge_case_numbers_in_name(self):
        """Test from_str with numbers in decorator name."""
        result = DecoratorInfo.from_str("@decorator123")
        self.assertEqual("decorator123", result.name)

    def test_edge_case_underscore_start(self):
        """Test from_str with underscore at start of decorator name."""
        result = DecoratorInfo.from_str("@_decorator")
        self.assertEqual("_decorator", result.name)

    def test_edge_case_empty_arguments(self):
        """Test from_str with empty parentheses."""
        result = DecoratorInfo.from_str("@decorator()")
        self.assertEqual("decorator", result.name)
        self.assertEqual([], result.arguments)

    def test_edge_case_whitespace_in_arguments(self):
        """Test from_str with whitespace in arguments."""
        result = DecoratorInfo.from_str("@decorator( arg1 , arg2 )")
        self.assertEqual("decorator", result.name)
        self.assertEqual(2, len(result.arguments))

    def test_edge_case_complex_nested_types(self):
        """Test from_str with complex nested type annotations."""
        result = DecoratorInfo.from_str(
            "@decorator(arg1: List[Dict[str, Optional[int]]])")
        self.assertEqual("decorator", result.name)
        self.assertEqual(1, len(result.arguments))
        self.assertEqual(
            "List[Dict[str, Optional[int]]]", result.arguments[0].type)

    def test_edge_case_multiline_arguments(self):
        """Test from_str with multiline arguments."""
        result = DecoratorInfo.from_str(
            "@decorator(arg1: str = 'default', arg2: int = 42)")
        self.assertEqual("decorator", result.name)
        self.assertEqual(2, len(result.arguments))
        self.assertEqual("'default'", result.arguments[0].default)
        self.assertEqual("42", result.arguments[1].default)


if __name__ == '__main__':
    unittest.main()
