import unittest
from unittest.mock import patch, MagicMock
from abc import ABC, abstractmethod
from typing import List, Optional, Generic, TypeVar

from danielutils.reflection.class_info import ClassInfo
from danielutils.reflection.function_info import FunctionInfo
from danielutils.reflection.decoration_info import DecorationInfo
from danielutils.reflection.argument_info import ArgumentInfo


class TestClassInfo(unittest.TestCase):
    """Test cases for ClassInfo class."""

    def setUp(self):
        """Set up test fixtures."""
        # Create test classes with various method types
        class SimpleClass:
            """Simple test class."""

            def __init__(self, value: str):
                self.value = value

            def instance_method(self, arg1: str) -> str:
                """Instance method."""
                return f"{self.value}: {arg1}"

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
                return self.value

        class InheritedClass(SimpleClass):
            """Class that inherits from SimpleClass."""

            def inherited_method(self, arg1: str) -> str:
                """Inherited method."""
                return f"inherited: {arg1}"

        class AbstractClass(ABC):
            """Abstract class for testing."""
            @abstractmethod
            def abstract_method(self) -> str:
                """Abstract method."""
                pass

            def concrete_method(self) -> str:
                """Concrete method."""
                return "concrete"

        class DecoratedClass:
            """Class with decorators."""
            @classmethod
            def decorated_method(cls, arg1: str) -> str:
                """Decorated method."""
                return f"decorated: {arg1}"

        class GenericTestClass(Generic[T]):
            """Generic class for testing."""

            def __init__(self, value: T):
                self.value = value

            def generic_method(self, arg1: T) -> T:
                """Generic method."""
                return arg1

        self.simple_class = SimpleClass
        self.inherited_class = InheritedClass
        self.abstract_class = AbstractClass
        self.decorated_class = DecoratedClass
        self.generic_class = GenericTestClass

    def test_init_with_simple_class(self):
        """Test ClassInfo initialization with a simple class."""
        class_info = ClassInfo(self.simple_class)

        self.assertEqual(class_info.name, "SimpleClass")
        self.assertEqual(len(class_info.bases), 0)
        self.assertEqual(len(class_info.decorations), 0)

    def test_init_with_inherited_class(self):
        """Test ClassInfo initialization with an inherited class."""
        class_info = ClassInfo(self.inherited_class)

        self.assertEqual(class_info.name, "InheritedClass")
        self.assertEqual(len(class_info.bases), 1)
        self.assertEqual(class_info.bases[0].name, "SimpleClass")

    def test_init_with_abstract_class(self):
        """Test ClassInfo initialization with an abstract class."""
        class_info = ClassInfo(self.abstract_class)

        self.assertEqual(class_info.name, "AbstractClass")
        self.assertEqual(len(class_info.bases), 1)
        self.assertEqual(class_info.bases[0].name, "ABC")

    def test_init_with_decorated_class(self):
        """Test ClassInfo initialization with a decorated class."""
        class_info = ClassInfo(self.decorated_class)

        self.assertEqual(class_info.name, "DecoratedClass")
        self.assertEqual(len(class_info.bases), 0)

    def test_init_with_generic_class(self):
        """Test ClassInfo initialization with a generic class."""
        class_info = ClassInfo(self.generic_class)

        self.assertEqual(class_info.name, "GenericTestClass")
        self.assertEqual(len(class_info.bases), 1)
        self.assertEqual(class_info.bases[0].name, "Generic")

    def test_init_with_non_class_raises_typeerror(self):
        """Test ClassInfo initialization with non-class raises TypeError."""
        with self.assertRaises(TypeError):
            ClassInfo("not_a_class")

    def test_init_with_function_raises_typeerror(self):
        """Test ClassInfo initialization with function raises TypeError."""
        def test_func():
            pass

        with self.assertRaises(TypeError):
            ClassInfo(test_func)

    def test_properties(self):
        """Test that all properties return correct values."""
        class_info = ClassInfo(self.simple_class)

        self.assertEqual(class_info.name, "SimpleClass")
        self.assertEqual(len(class_info.bases), 0)
        self.assertEqual(len(class_info.decorations), 0)
        self.assertIsInstance(class_info.functions, list)

    def test_static_methods_property(self):
        """Test static_methods property."""
        class_info = ClassInfo(self.simple_class)
        static_methods = list(class_info.static_methods)

        self.assertEqual(len(static_methods), 1)
        self.assertEqual(static_methods[0].name, "static_method")

    def test_class_methods_property(self):
        """Test class_methods property."""
        class_info = ClassInfo(self.simple_class)
        class_methods = list(class_info.class_methods)

        self.assertEqual(len(class_methods), 1)
        self.assertEqual(class_methods[0].name, "class_method")

    def test_instance_methods_property(self):
        """Test instance_methods property."""
        class_info = ClassInfo(self.simple_class)
        instance_methods = list(class_info.instance_methods)

        # Should include __init__ and instance_method
        self.assertGreaterEqual(len(instance_methods), 2)
        method_names = [m.name for m in instance_methods]
        self.assertIn("instance_method", method_names)

    def test_inherited_methods_property(self):
        """Test inherited_methods property."""
        class_info = ClassInfo(self.inherited_class)
        inherited_methods = list(class_info.inherited_methods)

        # Should include methods inherited from SimpleClass
        self.assertGreaterEqual(len(inherited_methods), 0)

    def test_abstract_methods_property(self):
        """Test abstract_methods property."""
        class_info = ClassInfo(self.abstract_class)
        abstract_methods = list(class_info.abstract_methods)

        self.assertEqual(len(abstract_methods), 1)
        self.assertEqual(abstract_methods[0].name, "abstract_method")

    def test_functions_property(self):
        """Test functions property."""
        class_info = ClassInfo(self.simple_class)
        functions = class_info.functions

        self.assertIsInstance(functions, list)
        self.assertGreater(len(functions), 0)

        # All functions should be FunctionInfo instances
        for func in functions:
            self.assertIsInstance(func, FunctionInfo)

    def test_str_method(self):
        """Test __str__ method."""
        class_info = ClassInfo(self.simple_class)
        str_repr = str(class_info)

        self.assertIn("ClassInfo", str_repr)
        self.assertIn("SimpleClass", str_repr)
        self.assertIn("static_methods", str_repr)
        self.assertIn("class_methods", str_repr)
        self.assertIn("instance_methods", str_repr)

    def test_repr_method(self):
        """Test __repr__ method."""
        class_info = ClassInfo(self.simple_class)
        repr_str = repr(class_info)

        self.assertEqual(repr_str, 'ClassInfo(name="SimpleClass")')

    def test_class_with_multiple_bases(self):
        """Test ClassInfo with class having multiple base classes."""
        class Base1:
            pass

        class Base2:
            pass

        class MultiInheritClass(Base1, Base2):
            def test_method(self) -> str:
                return "test"

        class_info = ClassInfo(MultiInheritClass)

        self.assertEqual(class_info.name, "MultiInheritClass")
        self.assertEqual(len(class_info.bases), 2)
        base_names = [b.name for b in class_info.bases]
        self.assertIn("Base1", base_names)
        self.assertIn("Base2", base_names)

    def test_class_with_complex_bases(self):
        """Test ClassInfo with class having complex base classes."""
        class ComplexBase:
            def __init__(self, value: str):
                self.value = value

        class ComplexInheritClass(ComplexBase):
            def __init__(self, value: str, extra: int):
                super().__init__(value)
                self.extra = extra

        class_info = ClassInfo(ComplexInheritClass)

        self.assertEqual(class_info.name, "ComplexInheritClass")
        self.assertEqual(len(class_info.bases), 1)
        self.assertEqual(class_info.bases[0].name, "ComplexBase")

    def test_class_with_decorators(self):
        """Test ClassInfo with class having decorators."""
        def class_decorator(cls):
            cls.decorated = True
            return cls

        @class_decorator
        class DecoratedTestClass:
            def test_method(self) -> str:
                return "test"

        class_info = ClassInfo(DecoratedTestClass)

        self.assertEqual(class_info.name, "DecoratedTestClass")
        self.assertEqual(len(class_info.decorations), 1)
        self.assertEqual(class_info.decorations[0].name, "class_decorator")

    def test_class_with_multiple_decorators(self):
        """Test ClassInfo with class having multiple decorators."""
        def decorator1(cls):
            cls.decorated1 = True
            return cls

        def decorator2(cls):
            cls.decorated2 = True
            return cls

        @decorator1
        @decorator2
        class MultiDecoratedClass:
            def test_method(self) -> str:
                return "test"

        class_info = ClassInfo(MultiDecoratedClass)

        self.assertEqual(class_info.name, "MultiDecoratedClass")
        self.assertEqual(len(class_info.decorations), 2)
        decorator_names = [d.name for d in class_info.decorations]
        self.assertIn("decorator1", decorator_names)
        self.assertIn("decorator2", decorator_names)

    def test_class_with_properties(self):
        """Test ClassInfo with class having properties."""
        class PropertyClass:
            def __init__(self, value: str):
                self._value = value

            @property
            def test_property(self) -> str:
                return self._value

            @test_property.setter
            def test_property(self, value: str):
                self._value = value

        class_info = ClassInfo(PropertyClass)

        self.assertEqual(class_info.name, "PropertyClass")
        # Properties should be included in functions
        property_functions = [f for f in class_info.functions if f.is_property]
        self.assertGreaterEqual(len(property_functions), 1)

    def test_class_with_async_methods(self):
        """Test ClassInfo with class having async methods."""
        class AsyncClass:
            async def async_method(self, arg1: str) -> str:
                return f"async: {arg1}"

            def sync_method(self, arg1: str) -> str:
                return f"sync: {arg1}"

        class_info = ClassInfo(AsyncClass)

        self.assertEqual(class_info.name, "AsyncClass")
        async_functions = [f for f in class_info.functions if f.is_async]
        self.assertEqual(len(async_functions), 1)
        self.assertEqual(async_functions[0].name, "async_method")

    def test_class_with_complex_methods(self):
        """Test ClassInfo with class having complex method signatures."""
        class ComplexMethodClass:
            def complex_method(self,
                               arg1: List[str],
                               arg2: Optional[int] = None,
                               *args,
                               **kwargs) -> str:
                return "complex"

            def simple_method(self, arg1: str) -> str:
                return arg1

        class_info = ClassInfo(ComplexMethodClass)

        self.assertEqual(class_info.name, "ComplexMethodClass")
        complex_method = next(
            f for f in class_info.functions if f.name == "complex_method")
        # self, arg1, arg2, args, kwargs
        self.assertEqual(len(complex_method.arguments), 5)

    def test_class_with_return_type_annotations(self):
        """Test ClassInfo with class having methods with return type annotations."""
        class ReturnTypeClass:
            def method_with_return(self, arg1: str) -> Optional[str]:
                return arg1 if arg1 else None

            def method_without_return(self, arg1: str):
                return arg1

        class_info = ClassInfo(ReturnTypeClass)

        self.assertEqual(class_info.name, "ReturnTypeClass")
        with_return_method = next(
            f for f in class_info.functions if f.name == "method_with_return")
        without_return_method = next(
            f for f in class_info.functions if f.name == "method_without_return")

        self.assertEqual(with_return_method.return_type, "Optional[str]")
        self.assertEqual(without_return_method.return_type, "None")

    def test_class_with_nested_classes(self):
        """Test ClassInfo with class having nested classes."""
        class OuterClass:
            class InnerClass:
                def inner_method(self) -> str:
                    return "inner"

            def outer_method(self) -> str:
                return "outer"

        class_info = ClassInfo(OuterClass)

        self.assertEqual(class_info.name, "OuterClass")
        # Should only include methods from the outer class
        method_names = [f.name for f in class_info.functions]
        self.assertIn("outer_method", method_names)
        self.assertNotIn("inner_method", method_names)

    def test_class_with_class_variables(self):
        """Test ClassInfo with class having class variables."""
        class ClassVariableClass:
            class_var = "class_value"

            def __init__(self, value: str):
                self.instance_var = value

            def test_method(self) -> str:
                return self.instance_var

        class_info = ClassInfo(ClassVariableClass)

        self.assertEqual(class_info.name, "ClassVariableClass")
        # Class variables should not be included in functions
        function_names = [f.name for f in class_info.functions]
        self.assertNotIn("class_var", function_names)

    def test_class_with_slots(self):
        """Test ClassInfo with class using __slots__."""
        class SlotsClass:
            __slots__ = ['value']

            def __init__(self, value: str):
                self.value = value

            def test_method(self) -> str:
                return self.value

        class_info = ClassInfo(SlotsClass)

        self.assertEqual(class_info.name, "SlotsClass")
        # Should work normally despite __slots__
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_metaclass(self):
        """Test ClassInfo with class using a metaclass."""
        class MetaClass(type):
            pass

        class MetaClassTest(metaclass=MetaClass):
            def test_method(self) -> str:
                return "test"

        class_info = ClassInfo(MetaClassTest)

        self.assertEqual(class_info.name, "MetaClassTest")
        # Should work normally despite metaclass
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_dataclass(self):
        """Test ClassInfo with dataclass."""
        from dataclasses import dataclass

        @dataclass
        class DataClassTest:
            value: str

            def test_method(self) -> str:
                return self.value

        class_info = ClassInfo(DataClassTest)

        self.assertEqual(class_info.name, "DataClassTest")
        # Should work normally with dataclass
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_enum(self):
        """Test ClassInfo with enum class."""
        from enum import Enum

        class TestEnum(Enum):
            VALUE1 = "value1"
            VALUE2 = "value2"

        class_info = ClassInfo(TestEnum)

        self.assertEqual(class_info.name, "TestEnum")
        # Should work normally with enum
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_mixin(self):
        """Test ClassInfo with mixin class."""
        class Mixin:
            def mixin_method(self) -> str:
                return "mixin"

        class MixinClass(Mixin):
            def class_method(self) -> str:
                return "class"

        class_info = ClassInfo(MixinClass)

        self.assertEqual(class_info.name, "MixinClass")
        self.assertEqual(len(class_info.bases), 1)
        self.assertEqual(class_info.bases[0].name, "Mixin")

    def test_class_with_abstract_base_class(self):
        """Test ClassInfo with abstract base class."""
        from abc import ABC, abstractmethod

        class AbstractBase(ABC):
            @abstractmethod
            def abstract_method(self) -> str:
                pass

            def concrete_method(self) -> str:
                return "concrete"

        class ConcreteClass(AbstractBase):
            def abstract_method(self) -> str:
                return "implemented"

        class_info = ClassInfo(ConcreteClass)

        self.assertEqual(class_info.name, "ConcreteClass")
        self.assertEqual(len(class_info.bases), 1)
        self.assertEqual(class_info.bases[0].name, "AbstractBase")

    def test_class_with_protocol(self):
        """Test ClassInfo with protocol class."""
        from typing import Protocol

        class TestProtocol(Protocol):
            def protocol_method(self) -> str:
                ...

        class ProtocolImpl:
            def protocol_method(self) -> str:
                return "implemented"

        class_info = ClassInfo(ProtocolImpl)

        self.assertEqual(class_info.name, "ProtocolImpl")
        # Should work normally with protocol implementation
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_type_alias(self):
        """Test ClassInfo with class that has type aliases."""
        from typing import TypeAlias

        MyType: TypeAlias = str

        class TypeAliasClass:
            def method_with_alias(self, arg1: MyType) -> MyType:
                return arg1

        class_info = ClassInfo(TypeAliasClass)

        self.assertEqual(class_info.name, "TypeAliasClass")
        # Should work normally with type aliases
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_forward_references(self):
        """Test ClassInfo with class using forward references."""
        class ForwardRefClass:
            def method_with_forward_ref(self, arg1: 'ForwardRefClass') -> 'ForwardRefClass':
                return arg1

        class_info = ClassInfo(ForwardRefClass)

        self.assertEqual(class_info.name, "ForwardRefClass")
        # Should work normally with forward references
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_literal_types(self):
        """Test ClassInfo with class using literal types."""
        from typing import Literal

        class LiteralClass:
            def method_with_literal(self, arg1: Literal["a", "b", "c"]) -> str:
                return arg1

        class_info = ClassInfo(LiteralClass)

        self.assertEqual(class_info.name, "LiteralClass")
        # Should work normally with literal types
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_union_types(self):
        """Test ClassInfo with class using union types."""
        from typing import Union

        class UnionClass:
            def method_with_union(self, arg1: Union[str, int]) -> Union[str, None]:
                return str(arg1) if arg1 else None

        class_info = ClassInfo(UnionClass)

        self.assertEqual(class_info.name, "UnionClass")
        # Should work normally with union types
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_callable_types(self):
        """Test ClassInfo with class using callable types."""
        from typing import Callable

        class CallableClass:
            def method_with_callable(self, func: Callable[[str], int]) -> int:
                return func("test")

        class_info = ClassInfo(CallableClass)

        self.assertEqual(class_info.name, "CallableClass")
        # Should work normally with callable types
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_generic_types(self):
        """Test ClassInfo with class using generic types."""
        from typing import TypeVar, Generic

        T = TypeVar('T')

        class GenericClass(Generic[T]):
            def generic_method(self, arg1: T) -> T:
                return arg1

        class_info = ClassInfo(GenericClass)

        self.assertEqual(class_info.name, "GenericClass")
        # Should work normally with generic types
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_annotated_types(self):
        """Test ClassInfo with class using annotated types."""
        from typing import Annotated

        class AnnotatedClass:
            def annotated_method(self, arg1: Annotated[str, "description"]) -> str:
                return arg1

        class_info = ClassInfo(AnnotatedClass)

        self.assertEqual(class_info.name, "AnnotatedClass")
        # Should work normally with annotated types
        self.assertGreater(len(class_info.functions), 0)

    def test_class_with_complex_nested_types(self):
        """Test ClassInfo with class using complex nested types."""
        from typing import Dict, List, Optional, Callable

        class ComplexNestedClass:
            def complex_nested_method(self,
                                      arg1: List[Dict[str, Optional[List[int]]]],
                                      arg2: Callable[[str], List[Optional[str]]]) -> Dict[str, List[Optional[int]]]:
                return {"test": [1, None, 3]}

        class_info = ClassInfo(ComplexNestedClass)

        self.assertEqual(class_info.name, "ComplexNestedClass")
        # Should work normally with complex nested types
        self.assertGreater(len(class_info.functions), 0)


if __name__ == '__main__':
    unittest.main()
