import unittest
from unittest.mock import patch, MagicMock

from danielutils.reflection.info_classes.argument_info import ArgumentInfo


class TestArgumentInfo(unittest.TestCase):
    """Test cases for ArgumentInfo class."""

    def test_init_with_all_parameters(self):
        """Test ArgumentInfo initialization with all parameters."""
        arg_info = ArgumentInfo(
            name="test_arg",
            type="str",
            default="default_value",
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=["param1", "param2"]
        )

        self.assertEqual("test_arg", arg_info.name)
        self.assertEqual("str", arg_info.type)
        self.assertEqual("default_value", arg_info.default)
        self.assertFalse(arg_info.is_kwargs)
        self.assertFalse(arg_info.is_args)
        self.assertFalse(arg_info.is_kwargs_only)
        self.assertEqual(["param1", "param2"], arg_info.parameters)

    def test_init_with_minimal_parameters(self):
        """Test ArgumentInfo initialization with minimal parameters."""
        arg_info = ArgumentInfo(
            name=None,
            type=None,
            default=None,
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=None
        )

        self.assertIsNone(arg_info.name)
        self.assertIsNone(arg_info.type)
        self.assertIsNone(arg_info.default)
        self.assertFalse(arg_info.is_kwargs)
        self.assertFalse(arg_info.is_args)
        self.assertFalse(arg_info.is_kwargs_only)
        self.assertIsNone(arg_info.parameters)

    def test_properties(self):
        """Test that all properties return correct values."""
        arg_info = ArgumentInfo(
            name="test",
            type="int",
            default="42",
            is_kwargs=True,
            is_args=False,
            is_kwargs_only=False,
            parameters=["p1", "p2"]
        )

        self.assertEqual("test", arg_info.name)
        self.assertEqual("int", arg_info.type)
        self.assertEqual("42", arg_info.default)
        self.assertTrue(arg_info.is_kwargs)
        self.assertFalse(arg_info.is_args)
        self.assertFalse(arg_info.is_kwargs_only)
        self.assertEqual(["p1", "p2"], arg_info.parameters)

    def test_is_parameterized_with_parameters(self):
        """Test is_parameterized property with parameters."""
        arg_info = ArgumentInfo(
            name="test",
            type="List[str]",
            default=None,
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=["str"]
        )

        self.assertTrue(arg_info.is_parameterized)

    def test_is_parameterized_without_parameters(self):
        """Test is_parameterized property without parameters."""
        arg_info = ArgumentInfo(
            name="test",
            type="str",
            default=None,
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=None
        )

        self.assertFalse(arg_info.is_parameterized)

    def test_is_parameterized_with_empty_parameters(self):
        """Test is_parameterized property with empty parameters list."""
        arg_info = ArgumentInfo(
            name="test",
            type="str",
            default=None,
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=[]
        )

        self.assertFalse(arg_info.is_parameterized)

    def test_repr_with_all_fields(self):
        """Test __repr__ method with all fields populated."""
        arg_info = ArgumentInfo(
            name="test_arg",
            type="str",
            default="default",
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=["param1"]
        )

        expected = 'ArgumentInfo(name="test_arg", type=str, default=default, parameters=[\'param1\'])'
        self.assertEqual(repr(arg_info), expected)

    def test_repr_with_name_only(self):
        """Test __repr__ method with only name field."""
        arg_info = ArgumentInfo(
            name="test_arg",
            type=None,
            default=None,
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=None
        )

        expected = 'ArgumentInfo(name="test_arg")'
        self.assertEqual(repr(arg_info), expected)

    def test_repr_with_name_and_type(self):
        """Test __repr__ method with name and type fields."""
        arg_info = ArgumentInfo(
            name="test_arg",
            type="int",
            default=None,
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=None
        )

        expected = 'ArgumentInfo(name="test_arg", type=int)'
        self.assertEqual(repr(arg_info), expected)

    def test_repr_with_name_and_default(self):
        """Test __repr__ method with name and default fields."""
        arg_info = ArgumentInfo(
            name="test_arg",
            type=None,
            default="42",
            is_kwargs=False,
            is_args=False,
            is_kwargs_only=False,
            parameters=None
        )

        expected = 'ArgumentInfo(name="test_arg", default=42)'
        self.assertEqual(repr(arg_info), expected)

    def test_str_method(self):
        """Test __str__ method."""
        arg_info = ArgumentInfo("test", "str", None, False, False, False, None)
        self.assertEqual(str(arg_info), repr(arg_info))

    def test_from_str_simple_argument(self):
        """Test from_str with a simple argument."""
        result = ArgumentInfo.from_str("arg1")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertIsNone(result[0].type)
        self.assertIsNone(result[0].default)

    def test_from_str_typed_argument(self):
        """Test from_str with a typed argument."""
        result = ArgumentInfo.from_str("arg1: str")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("str", result[0].type)
        self.assertIsNone(result[0].default)

    def test_from_str_argument_with_default(self):
        """Test from_str with an argument with default value."""
        result = ArgumentInfo.from_str("arg1=42")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertIsNone(result[0].type)
        self.assertEqual("42", result[0].default)

    def test_from_str_typed_argument_with_default(self):
        """Test from_str with a typed argument with default value."""
        result = ArgumentInfo.from_str("arg1: int = 42")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("int", result[0].type)
        self.assertEqual("42", result[0].default)

    def test_from_str_multiple_arguments(self):
        """Test from_str with multiple arguments."""
        result = ArgumentInfo.from_str("arg1: str, arg2: int = 42")

        self.assertEqual(2, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("str", result[0].type)
        self.assertEqual("arg2", result[1].name)
        self.assertEqual("int", result[1].type)
        self.assertEqual("42", result[1].default)

    def test_from_str_args_argument(self):
        """Test from_str with *args argument."""
        result = ArgumentInfo.from_str("*args")

        self.assertEqual(1, len(result))
        self.assertEqual("args", result[0].name)
        self.assertTrue(result[0].is_args)
        self.assertFalse(result[0].is_kwargs)

    def test_from_str_kwargs_argument(self):
        """Test from_str with **kwargs argument."""
        result = ArgumentInfo.from_str("**kwargs")

        self.assertEqual(1, len(result))
        self.assertEqual("kwargs", result[0].name)
        self.assertTrue(result[0].is_kwargs)
        self.assertFalse(result[0].is_args)

    def test_from_str_kwargs_only_argument(self):
        """Test from_str with / (kwargs-only) argument."""
        result = ArgumentInfo.from_str("/")

        self.assertEqual(1, len(result))
        self.assertEqual("/", result[0].name)
        self.assertTrue(result[0].is_kwargs_only)

    def test_from_str_parameterized_type(self):
        """Test from_str with parameterized type."""
        result = ArgumentInfo.from_str("arg1: List[str]")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("List[str]", result[0].type)
        self.assertTrue(result[0].is_parameterized)

    def test_from_str_complex_parameterized_type(self):
        """Test from_str with complex parameterized type."""
        result = ArgumentInfo.from_str("arg1: Dict[str, List[int]]")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("Dict[str, List[int]]", result[0].type)

    def test_from_str_none_string(self):
        """Test from_str with None string."""
        result = ArgumentInfo.from_str(None)
        self.assertEqual(result, [])

    def test_from_str_empty_string(self):
        """Test from_str with empty string."""
        result = ArgumentInfo.from_str("")
        self.assertEqual(result, [])

    def test_from_str_whitespace_string(self):
        """Test from_str with whitespace only string."""
        result = ArgumentInfo.from_str("   ")
        self.assertEqual(result, [])

    def test_from_str_invalid_argument(self):
        """Test from_str with invalid argument raises ValueError."""
        with self.assertRaises(ValueError):
            ArgumentInfo.from_str("@invalid")

    def test_from_str_with_spaces(self):
        """Test from_str with arguments containing spaces."""
        result = ArgumentInfo.from_str(" arg1 : str = 42 , arg2 : int ")

        self.assertEqual(2, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("str", result[0].type)
        self.assertEqual("42", result[0].default)
        self.assertEqual("arg2", result[1].name)
        self.assertEqual("int", result[1].type)

    def test_from_str_with_string_default(self):
        """Test from_str with string default value."""
        result = ArgumentInfo.from_str("arg1: str = 'default'")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("str", result[0].type)
        self.assertEqual("'default'", result[0].default)

    def test_from_str_with_complex_default(self):
        """Test from_str with complex default value."""
        result = ArgumentInfo.from_str("arg1: dict = {'key': 'value'}")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("dict", result[0].type)
        self.assertEqual("{'key': 'value'}", result[0].default)

    def test_from_str_with_nested_brackets(self):
        """Test from_str with nested brackets in type annotations."""
        result = ArgumentInfo.from_str("arg1: List[Dict[str, Optional[int]]]")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("List[Dict[str, Optional[int]]]", result[0].type)

    def test_from_str_with_multiple_nested_types(self):
        """Test from_str with multiple arguments having nested types."""
        result = ArgumentInfo.from_str(
            "arg1: List[str], arg2: Dict[str, List[int]]")

        self.assertEqual(2, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("List[str]", result[0].type)
        self.assertEqual("arg2", result[1].name)
        self.assertEqual("Dict[str, List[int]]", result[1].type)

    def test_from_str_with_optional_type(self):
        """Test from_str with Optional type."""
        result = ArgumentInfo.from_str("arg1: Optional[str] = None")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("Optional[str]", result[0].type)
        self.assertEqual("None", result[0].default)

    def test_from_str_with_union_type(self):
        """Test from_str with Union type."""
        result = ArgumentInfo.from_str("arg1: Union[str, int]")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("Union[str, int]", result[0].type)

    def test_from_str_with_callable_type(self):
        """Test from_str with Callable type."""
        result = ArgumentInfo.from_str("arg1: Callable[[str], int]")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("Callable[[str], int]", result[0].type)

    def test_from_str_with_literal_type(self):
        """Test from_str with Literal type."""
        result = ArgumentInfo.from_str("arg1: Literal['a', 'b', 'c']")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("Literal['a', 'b', 'c']", result[0].type)

    def test_from_str_with_annotated_type(self):
        """Test from_str with Annotated type."""
        result = ArgumentInfo.from_str("arg1: Annotated[str, 'description']")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("Annotated[str, 'description']", result[0].type)

    def test_from_str_with_self_argument(self):
        """Test from_str with self argument."""
        result = ArgumentInfo.from_str("self")

        self.assertEqual(1, len(result))
        self.assertEqual("self", result[0].name)
        self.assertIsNone(result[0].type)

    def test_from_str_with_cls_argument(self):
        """Test from_str with cls argument."""
        result = ArgumentInfo.from_str("cls")

        self.assertEqual(1, len(result))
        self.assertEqual("cls", result[0].name)
        self.assertIsNone(result[0].type)

    def test_from_str_with_positional_only_argument(self):
        """Test from_str with positional-only argument."""
        result = ArgumentInfo.from_str("arg1, /, arg2")

        self.assertEqual(3, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertEqual("/", result[1].name)
        self.assertTrue(result[1].is_kwargs_only)
        self.assertEqual("arg2", result[2].name)

    def test_from_str_with_keyword_only_argument(self):
        """Test from_str with keyword-only argument."""
        result = ArgumentInfo.from_str("*, arg1")

        self.assertEqual(1, len(result))
        self.assertEqual("arg1", result[0].name)
        self.assertIsNone(result[0].type)

    def test_from_str_with_mixed_argument_types(self):
        """Test from_str with mixed argument types."""
        result = ArgumentInfo.from_str(
            "self, arg1: str, *args, arg2: int = 42, **kwargs")

        self.assertEqual(5, len(result))
        self.assertEqual("self", result[0].name)
        self.assertEqual("arg1", result[1].name)
        self.assertEqual("str", result[1].type)
        self.assertEqual("args", result[2].name)
        self.assertTrue(result[2].is_args)
        self.assertEqual("arg2", result[3].name)
        self.assertEqual("int", result[3].type)
        self.assertEqual("42", result[3].default)
        self.assertEqual("kwargs", result[4].name)
        self.assertTrue(result[4].is_kwargs)

    def test_parse_one_invalid_string(self):
        """Test _parse_one with invalid string raises ValueError."""
        with self.assertRaises(ValueError):
            ArgumentInfo._parse_one("@invalid")

    def test_parse_one_empty_string(self):
        """Test _parse_one with empty string raises ValueError."""
        with self.assertRaises(ValueError):
            ArgumentInfo._parse_one("")

    def test_parse_one_whitespace_string(self):
        """Test _parse_one with whitespace only string raises ValueError."""
        with self.assertRaises(ValueError):
            ArgumentInfo._parse_one("   ")

    def test_equality_same_arguments(self):
        """Test that ArgumentInfo instances with same data are equal."""
        arg1 = ArgumentInfo("test", "str", "default",
                            False, False, False, None)
        arg2 = ArgumentInfo("test", "str", "default",
                            False, False, False, None)

        self.assertEqual(arg1.name, arg2.name)
        self.assertEqual(arg1.type, arg2.type)
        self.assertEqual(arg1.default, arg2.default)

    def test_equality_different_names(self):
        """Test that ArgumentInfo instances with different names are not equal."""
        arg1 = ArgumentInfo("test1", "str", "default",
                            False, False, False, None)
        arg2 = ArgumentInfo("test2", "str", "default",
                            False, False, False, None)

        self.assertNotEqual(arg1.name, arg2.name)

    def test_equality_different_types(self):
        """Test that ArgumentInfo instances with different types are not equal."""
        arg1 = ArgumentInfo("test", "str", "default",
                            False, False, False, None)
        arg2 = ArgumentInfo("test", "int", "default",
                            False, False, False, None)

        self.assertEqual(arg1.name, arg2.name)
        self.assertNotEqual(arg1.type, arg2.type)

    def test_equality_different_defaults(self):
        """Test that ArgumentInfo instances with different defaults are not equal."""
        arg1 = ArgumentInfo("test", "str", "default1",
                            False, False, False, None)
        arg2 = ArgumentInfo("test", "str", "default2",
                            False, False, False, None)

        self.assertEqual(arg1.name, arg2.name)
        self.assertNotEqual(arg1.default, arg2.default)


class TestArgumentInfoDecoratorContext(unittest.TestCase):
    """Test cases for ArgumentInfo when parsing decorator call arguments (literal values).

    This differs from definition context where arguments have names, types, and defaults.
    In decorator context, we parse actual literal values passed to decorators.
    """

    def test_from_str_string_literal_single_quotes(self):
        """Test from_str with string literal in single quotes (decorator argument)."""
        result = ArgumentInfo.from_str("'test_string'")

        self.assertEqual(1, len(result))
        # String literal should be stored in default field
        # Name should be None since it's a literal value, not a parameter definition
        self.assertIn("test_string", result[0].default or "")

    def test_from_str_string_literal_double_quotes(self):
        """Test from_str with string literal in double quotes (decorator argument)."""
        result = ArgumentInfo.from_str('"test_string"')

        self.assertEqual(1, len(result))
        # String literal should be stored in default field
        self.assertIn("test_string", result[0].default or "")

    def test_from_str_numeric_literal(self):
        """Test from_str with numeric literal (decorator argument)."""
        result = ArgumentInfo.from_str("42")

        self.assertEqual(1, len(result))
        # Numeric literal should be stored in default field
        self.assertEqual("42", result[0].default)

    def test_from_str_boolean_literal(self):
        """Test from_str with boolean literal (decorator argument)."""
        result = ArgumentInfo.from_str("True")

        self.assertEqual(1, len(result))
        # Boolean literal should be stored in default field
        self.assertEqual("True", result[0].default)

    def test_from_str_none_literal(self):
        """Test from_str with None literal (decorator argument)."""
        result = ArgumentInfo.from_str("None")

        self.assertEqual(1, len(result))
        # None literal should be stored in default field
        self.assertEqual("None", result[0].default)

    def test_from_str_list_literal(self):
        """Test from_str with list literal (decorator argument)."""
        result = ArgumentInfo.from_str("[1, 2, 3]")

        self.assertEqual(1, len(result))
        # List literal should be stored in default field
        self.assertIn("1", result[0].default or "")
        self.assertIn("2", result[0].default or "")
        self.assertIn("3", result[0].default or "")

    def test_from_str_dict_literal(self):
        """Test from_str with dict literal (decorator argument)."""
        result = ArgumentInfo.from_str("{'key': 'value'}")

        self.assertEqual(1, len(result))
        # Dict literal should be stored in default field
        self.assertIn("key", result[0].default or "")
        self.assertIn("value", result[0].default or "")

    def test_from_str_string_with_quotes_inside(self):
        """Test from_str with string containing quotes (decorator argument)."""
        result = ArgumentInfo.from_str('"test\\"string"')

        self.assertEqual(1, len(result))
        # String with escaped quotes should be parsed correctly
        self.assertIsNotNone(result[0].default)

    def test_from_str_empty_string_literal(self):
        """Test from_str with empty string literal (decorator argument)."""
        result = ArgumentInfo.from_str('""')

        self.assertEqual(1, len(result))
        # Empty string should be parsed
        self.assertIsNotNone(result[0].default)

    def test_from_str_complex_expression(self):
        """Test from_str with complex expression (decorator argument)."""
        result = ArgumentInfo.from_str("some_function(1, 2)")

        self.assertEqual(1, len(result))
        # Complex expression should be stored in default field
        self.assertIsNotNone(result[0].default)
        self.assertIn("some_function", result[0].default or "")


if __name__ == '__main__':
    unittest.main()
