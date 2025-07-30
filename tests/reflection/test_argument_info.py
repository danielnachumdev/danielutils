import unittest
from unittest.mock import patch, MagicMock

from danielutils.reflection.argument_info import ArgumentInfo


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

        self.assertEqual(arg_info.name, "test_arg")
        self.assertEqual(arg_info.type, "str")
        self.assertEqual(arg_info.default, "default_value")
        self.assertFalse(arg_info.is_kwargs)
        self.assertFalse(arg_info.is_args)
        self.assertFalse(arg_info.is_kwargs_only)
        self.assertEqual(arg_info.parameters, ["param1", "param2"])

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

        self.assertEqual(arg_info.name, "test")
        self.assertEqual(arg_info.type, "int")
        self.assertEqual(arg_info.default, "42")
        self.assertTrue(arg_info.is_kwargs)
        self.assertFalse(arg_info.is_args)
        self.assertFalse(arg_info.is_kwargs_only)
        self.assertEqual(arg_info.parameters, ["p1", "p2"])

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

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertIsNone(result[0].type)
        self.assertIsNone(result[0].default)

    def test_from_str_typed_argument(self):
        """Test from_str with a typed argument."""
        result = ArgumentInfo.from_str("arg1: str")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "str")
        self.assertIsNone(result[0].default)

    def test_from_str_argument_with_default(self):
        """Test from_str with an argument with default value."""
        result = ArgumentInfo.from_str("arg1=42")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertIsNone(result[0].type)
        self.assertEqual(result[0].default, "42")

    def test_from_str_typed_argument_with_default(self):
        """Test from_str with a typed argument with default value."""
        result = ArgumentInfo.from_str("arg1: int = 42")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "int")
        self.assertEqual(result[0].default, "42")

    def test_from_str_multiple_arguments(self):
        """Test from_str with multiple arguments."""
        result = ArgumentInfo.from_str("arg1: str, arg2: int = 42")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "str")
        self.assertEqual(result[1].name, "arg2")
        self.assertEqual(result[1].type, "int")
        self.assertEqual(result[1].default, "42")

    def test_from_str_args_argument(self):
        """Test from_str with *args argument."""
        result = ArgumentInfo.from_str("*args")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "args")
        self.assertTrue(result[0].is_args)
        self.assertFalse(result[0].is_kwargs)

    def test_from_str_kwargs_argument(self):
        """Test from_str with **kwargs argument."""
        result = ArgumentInfo.from_str("**kwargs")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "kwargs")
        self.assertTrue(result[0].is_kwargs)
        self.assertFalse(result[0].is_args)

    def test_from_str_kwargs_only_argument(self):
        """Test from_str with / (kwargs-only) argument."""
        result = ArgumentInfo.from_str("/")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "/")
        self.assertTrue(result[0].is_kwargs_only)

    def test_from_str_parameterized_type(self):
        """Test from_str with parameterized type."""
        result = ArgumentInfo.from_str("arg1: List[str]")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "List[str]")
        self.assertTrue(result[0].is_parameterized)

    def test_from_str_complex_parameterized_type(self):
        """Test from_str with complex parameterized type."""
        result = ArgumentInfo.from_str("arg1: Dict[str, List[int]]")

        self.assertEqual(len(result), 1)
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

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "str")
        self.assertEqual(result[0].default, "42")
        self.assertEqual(result[1].name, "arg2")
        self.assertEqual(result[1].type, "int")

    def test_from_str_with_string_default(self):
        """Test from_str with string default value."""
        result = ArgumentInfo.from_str("arg1: str = 'default'")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "str")
        self.assertEqual(result[0].default, "'default'")

    def test_from_str_with_complex_default(self):
        """Test from_str with complex default value."""
        result = ArgumentInfo.from_str("arg1: dict = {'key': 'value'}")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "dict")
        self.assertEqual(result[0].default, "{'key': 'value'}")

    def test_from_str_with_nested_brackets(self):
        """Test from_str with nested brackets in type annotations."""
        result = ArgumentInfo.from_str("arg1: List[Dict[str, Optional[int]]]")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "List[Dict[str, Optional[int]]]")

    def test_from_str_with_multiple_nested_types(self):
        """Test from_str with multiple arguments having nested types."""
        result = ArgumentInfo.from_str(
            "arg1: List[str], arg2: Dict[str, List[int]]")

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "List[str]")
        self.assertEqual(result[1].name, "arg2")
        self.assertEqual(result[1].type, "Dict[str, List[int]]")

    def test_from_str_with_optional_type(self):
        """Test from_str with Optional type."""
        result = ArgumentInfo.from_str("arg1: Optional[str] = None")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "Optional[str]")
        self.assertEqual(result[0].default, "None")

    def test_from_str_with_union_type(self):
        """Test from_str with Union type."""
        result = ArgumentInfo.from_str("arg1: Union[str, int]")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "Union[str, int]")

    def test_from_str_with_callable_type(self):
        """Test from_str with Callable type."""
        result = ArgumentInfo.from_str("arg1: Callable[[str], int]")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "Callable[[str], int]")

    def test_from_str_with_literal_type(self):
        """Test from_str with Literal type."""
        result = ArgumentInfo.from_str("arg1: Literal['a', 'b', 'c']")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "Literal['a', 'b', 'c']")

    def test_from_str_with_annotated_type(self):
        """Test from_str with Annotated type."""
        result = ArgumentInfo.from_str("arg1: Annotated[str, 'description']")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[0].type, "Annotated[str, 'description']")

    def test_from_str_with_self_argument(self):
        """Test from_str with self argument."""
        result = ArgumentInfo.from_str("self")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "self")
        self.assertIsNone(result[0].type)

    def test_from_str_with_cls_argument(self):
        """Test from_str with cls argument."""
        result = ArgumentInfo.from_str("cls")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "cls")
        self.assertIsNone(result[0].type)

    def test_from_str_with_positional_only_argument(self):
        """Test from_str with positional-only argument."""
        result = ArgumentInfo.from_str("arg1, /, arg2")

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].name, "arg1")
        self.assertEqual(result[1].name, "/")
        self.assertTrue(result[1].is_kwargs_only)
        self.assertEqual(result[2].name, "arg2")

    def test_from_str_with_keyword_only_argument(self):
        """Test from_str with keyword-only argument."""
        result = ArgumentInfo.from_str("*, arg1")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name, "arg1")
        self.assertIsNone(result[0].type)

    def test_from_str_with_mixed_argument_types(self):
        """Test from_str with mixed argument types."""
        result = ArgumentInfo.from_str(
            "self, arg1: str, *args, arg2: int = 42, **kwargs")

        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].name, "self")
        self.assertEqual(result[1].name, "arg1")
        self.assertEqual(result[1].type, "str")
        self.assertEqual(result[2].name, "args")
        self.assertTrue(result[2].is_args)
        self.assertEqual(result[3].name, "arg2")
        self.assertEqual(result[3].type, "int")
        self.assertEqual(result[3].default, "42")
        self.assertEqual(result[4].name, "kwargs")
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


if __name__ == '__main__':
    unittest.main()
