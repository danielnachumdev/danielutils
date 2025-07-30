import unittest
from unittest.mock import patch, MagicMock
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, TypeVar, Generic, Annotated, Dict, Literal

from danielutils.reflection.function_info import FunctionInfo
from danielutils.reflection.decoration_info import DecorationInfo
from danielutils.reflection.argument_info import ArgumentInfo


class TestFunctionInfo(unittest.TestCase):
    """Test cases for FunctionInfo class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a simple test class with various method types
        class TestClass:
            def simple_method(self, arg1: str, arg2: int = 42) -> str:
                """Simple instance method."""
                return f"{arg1}: {arg2}"
            
            @classmethod
            def class_method(cls, arg1: str) -> str:
                """Class method."""
                return f"class: {arg1}"
            
            @staticmethod
            def static_method(arg1: str) -> str:
                """Static method."""
                return f"static: {arg1}"
            
            @property
            def test_property(self) -> str:
                """Test property."""
                return "property_value"
            
            async def async_method(self, arg1: str) -> str:
                """Async method."""
                return f"async: {arg1}"
            
            def method_with_decorators(self, arg1: str) -> str:
                """Method with custom decorators."""
                return f"decorated: {arg1}"
            
            def method_with_return_type(self, arg1: str) -> Optional[str]:
                """Method with return type annotation."""
                return arg1 if arg1 else None

        self.test_class = TestClass()
        self.test_class_instance = TestClass()

    def test_init_with_simple_method(self):
        """Test FunctionInfo initialization with a simple method."""
        func_info = FunctionInfo(self.test_class.simple_method, self.test_class)
        
        self.assertEqual(func_info.name, "simple_method")
        self.assertFalse(func_info.is_async)
        self.assertFalse(func_info.is_property)
        self.assertEqual(len(func_info.arguments), 2)
        self.assertEqual(func_info.return_type, "str")

    def test_init_with_class_method(self):
        """Test FunctionInfo initialization with a class method."""
        func_info = FunctionInfo(self.test_class.class_method, self.test_class)
        
        self.assertEqual(func_info.name, "class_method")
        self.assertFalse(func_info.is_async)
        self.assertFalse(func_info.is_property)
        self.assertTrue(func_info.is_class_method)
        self.assertFalse(func_info.is_static_method)
        self.assertFalse(func_info.is_instance_method)

    def test_init_with_static_method(self):
        """Test FunctionInfo initialization with a static method."""
        func_info = FunctionInfo(self.test_class.static_method, self.test_class)
        
        self.assertEqual(func_info.name, "static_method")
        self.assertFalse(func_info.is_async)
        self.assertFalse(func_info.is_property)
        self.assertFalse(func_info.is_class_method)
        self.assertTrue(func_info.is_static_method)
        self.assertFalse(func_info.is_instance_method)

    def test_init_with_instance_method(self):
        """Test FunctionInfo initialization with an instance method."""
        func_info = FunctionInfo(self.test_class.simple_method, self.test_class)
        
        self.assertEqual(func_info.name, "simple_method")
        self.assertFalse(func_info.is_async)
        self.assertFalse(func_info.is_property)
        self.assertFalse(func_info.is_class_method)
        self.assertFalse(func_info.is_static_method)
        self.assertTrue(func_info.is_instance_method)

    def test_init_with_property(self):
        """Test FunctionInfo initialization with a property."""
        func_info = FunctionInfo(self.test_class.test_property, self.test_class)
        
        self.assertEqual(func_info.name, "test_property")
        self.assertFalse(func_info.is_async)
        self.assertTrue(func_info.is_property)

    def test_init_with_async_method(self):
        """Test FunctionInfo initialization with an async method."""
        func_info = FunctionInfo(self.test_class.async_method, self.test_class)
        
        self.assertEqual(func_info.name, "async_method")
        self.assertTrue(func_info.is_async)
        self.assertFalse(func_info.is_property)

    def test_init_with_method_with_return_type(self):
        """Test FunctionInfo initialization with method having return type."""
        func_info = FunctionInfo(self.test_class.method_with_return_type, self.test_class)
        
        self.assertEqual(func_info.name, "method_with_return_type")
        self.assertEqual(func_info.return_type, "Optional[str]")

    def test_properties(self):
        """Test that all properties return correct values."""
        func_info = FunctionInfo(self.test_class.simple_method, self.test_class)
        
        self.assertEqual(func_info.name, "simple_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 2)
        self.assertEqual(len(func_info.decorators), 0)

    def test_arguments_parsing(self):
        """Test that arguments are parsed correctly."""
        func_info = FunctionInfo(self.test_class.simple_method, self.test_class)
        
        self.assertEqual(len(func_info.arguments), 2)
        self.assertEqual(func_info.arguments[0].name, "self")
        self.assertEqual(func_info.arguments[1].name, "arg1")
        self.assertEqual(func_info.arguments[1].type, "str")
        self.assertEqual(func_info.arguments[2].name, "arg2")
        self.assertEqual(func_info.arguments[2].type, "int")
        self.assertEqual(func_info.arguments[2].default, "42")

    def test_decorators_parsing(self):
        """Test that decorators are parsed correctly."""
        # Create a method with decorators for testing
        class DecoratedClass:
            @classmethod
            @staticmethod
            def decorated_method(self, arg1: str) -> str:
                return arg1
        
        func_info = FunctionInfo(DecoratedClass.decorated_method, DecoratedClass)
        
        self.assertEqual(len(func_info.decorators), 2)
        decorator_names = [d.name for d in func_info.decorators]
        self.assertIn("classmethod", decorator_names)
        self.assertIn("staticmethod", decorator_names)

    def test_str_method(self):
        """Test __str__ method."""
        func_info = FunctionInfo(self.test_class.simple_method, self.test_class)
        str_repr = str(func_info)
        
        self.assertIn("FunctionInfo", str_repr)
        self.assertIn("simple_method", str_repr)
        self.assertIn("arguments", str_repr)

    def test_repr_method(self):
        """Test __repr__ method."""
        func_info = FunctionInfo(self.test_class.simple_method, self.test_class)
        repr_str = repr(func_info)
        
        self.assertEqual(repr_str, 'FunctionInfo(name="simple_method")')

    def test_is_inherited_property(self):
        """Test is_inherited property."""
        func_info = FunctionInfo(self.test_class.simple_method, self.test_class)
        
        # This should be False since the method is defined in the class itself
        self.assertFalse(func_info.is_inherited)

    def test_is_abstract_property(self):
        """Test is_abstract property."""
        # Create an abstract method for testing
        class AbstractClass(ABC):
            @abstractmethod
            def abstract_method(self) -> str:
                pass
        
        # Note: This will raise TypeError because abstract methods don't have source code
        with self.assertRaises(TypeError):
            FunctionInfo(AbstractClass.abstract_method, AbstractClass)

    def test_init_with_builtin_function(self):
        """Test FunctionInfo initialization with builtin function raises TypeError."""
        with self.assertRaises(TypeError):
            FunctionInfo(len, object)

    def test_init_with_lambda(self):
        """Test FunctionInfo initialization with lambda raises TypeError."""
        lambda_func = lambda x: x
        with self.assertRaises(TypeError):
            FunctionInfo(lambda_func, object)

    def test_init_with_c_function(self):
        """Test FunctionInfo initialization with C function raises TypeError."""
        with self.assertRaises(TypeError):
            FunctionInfo(print, object)

    def test_method_with_complex_arguments(self):
        """Test FunctionInfo with complex argument types."""
        class ComplexClass:
            def complex_method(self, 
                             arg1: List[str], 
                             arg2: Optional[int] = None,
                             *args,
                             **kwargs) -> str:
                return "complex"
        
        func_info = FunctionInfo(ComplexClass.complex_method, ComplexClass)
        
        self.assertEqual(func_info.name, "complex_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 5)  # self, arg1, arg2, args, kwargs

    def test_method_with_no_arguments(self):
        """Test FunctionInfo with method having no arguments."""
        class NoArgsClass:
            def no_args_method(self) -> str:
                return "no args"
        
        func_info = FunctionInfo(NoArgsClass.no_args_method, NoArgsClass)
        
        self.assertEqual(func_info.name, "no_args_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 1)  # only self

    def test_method_with_no_return_type(self):
        """Test FunctionInfo with method having no return type annotation."""
        class NoReturnClass:
            def no_return_method(self, arg1: str):
                return arg1
        
        func_info = FunctionInfo(NoReturnClass.no_return_method, NoReturnClass)
        
        self.assertEqual(func_info.name, "no_return_method")
        self.assertEqual(func_info.return_type, "None")

    def test_method_with_multiline_arguments(self):
        """Test FunctionInfo with method having multiline arguments."""
        class MultilineClass:
            def multiline_method(self,
                               arg1: str,
                               arg2: int = 42,
                               arg3: Optional[float] = None) -> str:
                return f"{arg1}: {arg2}: {arg3}"
        
        func_info = FunctionInfo(MultilineClass.multiline_method, MultilineClass)
        
        self.assertEqual(func_info.name, "multiline_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 4)  # self, arg1, arg2, arg3

    def test_method_with_complex_return_type(self):
        """Test FunctionInfo with method having complex return type."""
        class ComplexReturnClass:
            def complex_return_method(self, arg1: str) -> List[Optional[str]]:
                return [arg1, None]
        
        func_info = FunctionInfo(ComplexReturnClass.complex_return_method, ComplexReturnClass)
        
        self.assertEqual(func_info.name, "complex_return_method")
        self.assertEqual(func_info.return_type, "List[Optional[str]]")

    def test_method_with_decorators_and_arguments(self):
        """Test FunctionInfo with method having decorators and arguments."""
        class DecoratedArgsClass:
            @classmethod
            def decorated_with_args(cls, arg1: str, arg2: int = 10) -> str:
                return f"{arg1}: {arg2}"
        
        func_info = FunctionInfo(DecoratedArgsClass.decorated_with_args, DecoratedArgsClass)
        
        self.assertEqual(func_info.name, "decorated_with_args")
        self.assertEqual(func_info.return_type, "str")
        self.assertTrue(func_info.is_class_method)
        self.assertEqual(len(func_info.arguments), 3)  # cls, arg1, arg2

    def test_async_method_with_arguments(self):
        """Test FunctionInfo with async method having arguments."""
        class AsyncClass:
            async def async_with_args(self, arg1: str, arg2: int) -> str:
                return f"async {arg1}: {arg2}"
        
        func_info = FunctionInfo(AsyncClass.async_with_args, AsyncClass)
        
        self.assertEqual(func_info.name, "async_with_args")
        self.assertTrue(func_info.is_async)
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 3)  # self, arg1, arg2

    def test_property_with_getter(self):
        """Test FunctionInfo with property getter."""
        class PropertyClass:
            @property
            def test_prop(self) -> str:
                return "property_value"
        
        func_info = FunctionInfo(PropertyClass.test_prop, PropertyClass)
        
        self.assertEqual(func_info.name, "test_prop")
        self.assertTrue(func_info.is_property)
        self.assertEqual(func_info.return_type, "str")

    def test_method_with_positional_only_arguments(self):
        """Test FunctionInfo with method having positional-only arguments."""
        class PositionalClass:
            def positional_method(self, arg1, /, arg2, *, arg3) -> str:
                return f"{arg1}: {arg2}: {arg3}"
        
        func_info = FunctionInfo(PositionalClass.positional_method, PositionalClass)
        
        self.assertEqual(func_info.name, "positional_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 4)  # self, arg1, /, arg2, *, arg3

    def test_method_with_keyword_only_arguments(self):
        """Test FunctionInfo with method having keyword-only arguments."""
        class KeywordOnlyClass:
            def keyword_only_method(self, *, arg1: str, arg2: int = 42) -> str:
                return f"{arg1}: {arg2}"
        
        func_info = FunctionInfo(KeywordOnlyClass.keyword_only_method, KeywordOnlyClass)
        
        self.assertEqual(func_info.name, "keyword_only_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 3)  # self, *, arg1, arg2

    def test_method_with_union_type(self):
        """Test FunctionInfo with method having Union type."""
        class UnionClass:
            def union_method(self, arg1: str | int) -> str | None:
                return str(arg1) if arg1 else None
        
        func_info = FunctionInfo(UnionClass.union_method, UnionClass)
        
        self.assertEqual(func_info.name, "union_method")
        self.assertEqual(func_info.return_type, "str | None")
        self.assertEqual(len(func_info.arguments), 2)  # self, arg1

    def test_method_with_literal_type(self):
        """Test FunctionInfo with method having Literal type."""
        class LiteralClass:
            def literal_method(self, arg1: Literal["a", "b", "c"]) -> str:
                return arg1
        
        func_info = FunctionInfo(LiteralClass.literal_method, LiteralClass)
        
        self.assertEqual(func_info.name, "literal_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 2)  # self, arg1

    def test_method_with_callable_type(self):
        """Test FunctionInfo with method having Callable type."""
        class CallableClass:
            def callable_method(self, func: Callable[[str], int]) -> int:
                return func("test")
        
        func_info = FunctionInfo(CallableClass.callable_method, CallableClass)
        
        self.assertEqual(func_info.name, "callable_method")
        self.assertEqual(func_info.return_type, "int")
        self.assertEqual(len(func_info.arguments), 2)  # self, func

    def test_method_with_generic_type(self):
        """Test FunctionInfo with method having generic type."""
        from typing import TypeVar, Generic
        
        T = TypeVar('T')
        
        class GenericClass(Generic[T]):
            def generic_method(self, arg1: T) -> T:
                return arg1
        
        func_info = FunctionInfo(GenericClass.generic_method, GenericClass)
        
        self.assertEqual(func_info.name, "generic_method")
        self.assertEqual(func_info.return_type, "T")
        self.assertEqual(len(func_info.arguments), 2)  # self, arg1

    def test_method_with_annotated_type(self):
        """Test FunctionInfo with method having Annotated type."""
        from typing import Annotated
        
        class AnnotatedClass:
            def annotated_method(self, arg1: Annotated[str, "description"]) -> str:
                return arg1
        
        func_info = FunctionInfo(AnnotatedClass.annotated_method, AnnotatedClass)
        
        self.assertEqual(func_info.name, "annotated_method")
        self.assertEqual(func_info.return_type, "str")
        self.assertEqual(len(func_info.arguments), 2)  # self, arg1

    def test_method_with_complex_nested_types(self):
        """Test FunctionInfo with method having complex nested types."""
        class ComplexNestedClass:
            def complex_nested_method(self, 
                                   arg1: List[Dict[str, Optional[List[int]]]],
                                   arg2: Callable[[str], List[Optional[str]]]) -> Dict[str, List[Optional[int]]]:
                return {"test": [1, None, 3]}
        
        func_info = FunctionInfo(ComplexNestedClass.complex_nested_method, ComplexNestedClass)
        
        self.assertEqual(func_info.name, "complex_nested_method")
        self.assertEqual(func_info.return_type, "Dict[str, List[Optional[int]]]")
        self.assertEqual(len(func_info.arguments), 3)  # self, arg1, arg2


if __name__ == '__main__':
    unittest.main()
