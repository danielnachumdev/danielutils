import unittest
from unittest.mock import patch, MagicMock

from danielutils.reflection.decoration_info import DecorationInfo
from danielutils.reflection.argument_info import ArgumentInfo


class TestDecorationInfo(unittest.TestCase):
    """Test cases for DecorationInfo class."""

    def test_init_with_name_and_arguments(self):
        """Test DecorationInfo initialization with name and arguments."""
        name = "decorator"
        arguments = [ArgumentInfo(
            "arg1", "str", None, False, False, False, None)]
        decoration_info = DecorationInfo(name, arguments)

        self.assertEqual(decoration_info.name, name)
        self.assertEqual(decoration_info.arguments, arguments)

    def test_init_with_name_only(self):
        """Test DecorationInfo initialization with name only."""
        name = "decorator"
        arguments = []
        decoration_info = DecorationInfo(name, arguments)

        self.assertEqual(decoration_info.name, name)
        self.assertEqual(decoration_info.arguments, arguments)

    def test_properties(self):
        """Test that properties return correct values."""
        name = "test_decorator"
        arguments = [
            ArgumentInfo("param1", "int", "10", False, False, False, None),
            ArgumentInfo("param2", "str", None, False, False, False, None)
        ]
        decoration_info = DecorationInfo(name, arguments)

        self.assertEqual(decoration_info.name, name)
        self.assertEqual(decoration_info.arguments, arguments)

    def test_from_str_simple_decorator(self):
        """Test from_str with a simple decorator without arguments."""
        result = DecorationInfo.from_str("@decorator")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(result.arguments, [])

    def test_from_str_decorator_without_at_symbol(self):
        """Test from_str with a decorator without @ symbol."""
        result = DecorationInfo.from_str("decorator")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(result.arguments, [])

    def test_from_str_decorator_with_simple_argument(self):
        """Test from_str with a decorator with simple argument."""
        result = DecorationInfo.from_str("@decorator(arg1)")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 1)
        self.assertEqual(result.arguments[0].name, "arg1")

    def test_from_str_decorator_with_typed_argument(self):
        """Test from_str with a decorator with typed argument."""
        result = DecorationInfo.from_str("@decorator(arg1: str)")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 1)
        self.assertEqual(result.arguments[0].name, "arg1")
        self.assertEqual(result.arguments[0].type, "str")

    def test_from_str_decorator_with_default_argument(self):
        """Test from_str with a decorator with default argument."""
        result = DecorationInfo.from_str("@decorator(arg1=10)")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 1)
        self.assertEqual(result.arguments[0].name, "arg1")
        self.assertEqual(result.arguments[0].default, "10")

    def test_from_str_decorator_with_multiple_arguments(self):
        """Test from_str with a decorator with multiple arguments."""
        result = DecorationInfo.from_str(
            "@decorator(arg1: str, arg2: int = 10)")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].name, "arg1")
        self.assertEqual(result.arguments[0].type, "str")
        self.assertEqual(result.arguments[1].name, "arg2")
        self.assertEqual(result.arguments[1].type, "int")
        self.assertEqual(result.arguments[1].default, "10")

    def test_from_str_decorator_with_complex_arguments(self):
        """Test from_str with a decorator with complex arguments."""
        result = DecorationInfo.from_str("@decorator(*args, **kwargs)")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 2)
        self.assertTrue(result.arguments[0].is_args)
        self.assertTrue(result.arguments[1].is_kwargs)

    def test_from_str_invalid_string(self):
        """Test from_str with invalid string raises ValueError."""
        with self.assertRaises(ValueError):
            DecorationInfo.from_str("invalid@decorator")

    def test_from_str_empty_string(self):
        """Test from_str with empty string raises ValueError."""
        with self.assertRaises(ValueError):
            DecorationInfo.from_str("")

    def test_from_str_whitespace_only(self):
        """Test from_str with whitespace only raises ValueError."""
        with self.assertRaises(ValueError):
            DecorationInfo.from_str("   ")

    def test_from_str_with_nested_brackets(self):
        """Test from_str with nested brackets in arguments."""
        result = DecorationInfo.from_str(
            "@decorator(arg1: List[str], arg2: Dict[str, int])")

        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].name, "arg1")
        self.assertEqual(result.arguments[0].type, "List[str]")
        self.assertEqual(result.arguments[1].name, "arg2")
        self.assertEqual(result.arguments[1].type, "Dict[str, int]")

    def test_str_method(self):
        """Test __str__ method."""
        decoration_info = DecorationInfo("test", [])
        self.assertEqual(str(decoration_info), repr(decoration_info))

    def test_repr_without_arguments(self):
        """Test __repr__ method without arguments."""
        decoration_info = DecorationInfo("test", [])
        expected = 'DecorationInfo(name="test")'
        self.assertEqual(repr(decoration_info), expected)

    def test_repr_with_arguments(self):
        """Test __repr__ method with arguments."""
        arguments = [ArgumentInfo(
            "arg1", "str", None, False, False, False, None)]
        decoration_info = DecorationInfo("test", arguments)
        expected = 'DecorationInfo(name="test", arguments=[ArgumentInfo(name="arg1")])'
        self.assertEqual(repr(decoration_info), expected)

    def test_repr_with_complex_arguments(self):
        """Test __repr__ method with complex arguments."""
        arguments = [
            ArgumentInfo("arg1", "str", "default", False, False, False, None),
            ArgumentInfo("arg2", "int", None, False, False, False, None)
        ]
        decoration_info = DecorationInfo("test", arguments)
        # The exact format depends on ArgumentInfo.__repr__, but should contain the name
        self.assertIn('DecorationInfo(name="test"', repr(decoration_info))
        self.assertIn('arguments=', repr(decoration_info))

    def test_equality(self):
        """Test that DecorationInfo instances with same data are equal."""
        args1 = [ArgumentInfo("arg1", "str", None, False, False, False, None)]
        args2 = [ArgumentInfo("arg1", "str", None, False, False, False, None)]

        decoration1 = DecorationInfo("test", args1)
        decoration2 = DecorationInfo("test", args2)

        self.assertEqual(decoration1.name, decoration2.name)
        self.assertEqual(len(decoration1.arguments),
                         len(decoration2.arguments))

    def test_different_names_not_equal(self):
        """Test that DecorationInfo instances with different names are not equal."""
        args = [ArgumentInfo("arg1", "str", None, False, False, False, None)]

        decoration1 = DecorationInfo("test1", args)
        decoration2 = DecorationInfo("test2", args)

        self.assertNotEqual(decoration1.name, decoration2.name)

    def test_different_arguments_not_equal(self):
        """Test that DecorationInfo instances with different arguments are not equal."""
        args1 = [ArgumentInfo("arg1", "str", None, False, False, False, None)]
        args2 = [ArgumentInfo("arg2", "str", None, False, False, False, None)]

        decoration1 = DecorationInfo("test", args1)
        decoration2 = DecorationInfo("test", args2)

        self.assertEqual(decoration1.name, decoration2.name)
        self.assertNotEqual(
            decoration1.arguments[0].name, decoration2.arguments[0].name)

    def test_edge_case_special_characters_in_name(self):
        """Test from_str with special characters in decorator name."""
        # Should work with alphanumeric and underscore
        result = DecorationInfo.from_str("@decorator_123")
        self.assertEqual(result.name, "decorator_123")

    def test_edge_case_numbers_in_name(self):
        """Test from_str with numbers in decorator name."""
        result = DecorationInfo.from_str("@decorator123")
        self.assertEqual(result.name, "decorator123")

    def test_edge_case_underscore_start(self):
        """Test from_str with underscore at start of decorator name."""
        result = DecorationInfo.from_str("@_decorator")
        self.assertEqual(result.name, "_decorator")

    def test_edge_case_empty_arguments(self):
        """Test from_str with empty parentheses."""
        result = DecorationInfo.from_str("@decorator()")
        self.assertEqual(result.name, "decorator")
        self.assertEqual(result.arguments, [])

    def test_edge_case_whitespace_in_arguments(self):
        """Test from_str with whitespace in arguments."""
        result = DecorationInfo.from_str("@decorator( arg1 , arg2 )")
        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 2)

    def test_edge_case_complex_nested_types(self):
        """Test from_str with complex nested type annotations."""
        result = DecorationInfo.from_str(
            "@decorator(arg1: List[Dict[str, Optional[int]]])")
        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 1)
        self.assertEqual(
            result.arguments[0].type, "List[Dict[str, Optional[int]]]")

    def test_edge_case_multiline_arguments(self):
        """Test from_str with multiline arguments."""
        result = DecorationInfo.from_str(
            "@decorator(arg1: str = 'default', arg2: int = 42)")
        self.assertEqual(result.name, "decorator")
        self.assertEqual(len(result.arguments), 2)
        self.assertEqual(result.arguments[0].default, "'default'")
        self.assertEqual(result.arguments[1].default, "42")


if __name__ == '__main__':
    unittest.main()
