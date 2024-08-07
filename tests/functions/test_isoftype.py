import unittest
from typing import Union, Callable, Any, Optional, TypeVar, Iterable, ForwardRef, Literal, \
    AnyStr, Generator, Protocol, runtime_checkable, Dict, List, Tuple, Generic, Type

try:
    from danielutils.functions import isoftype  # type:ignore
    from danielutils.reflection import get_python_version  # type:ignore
    from danielutils import JavaInterface  # type:ignore
except:
    # python == 3.9.0
    from ...danielutils.functions import isoftype  # type:ignore
    from ...danielutils.reflection import get_python_version  # type:ignore
    from ...danielutils import JavaInterface  # type:ignore


class TestIsOfType(unittest.TestCase):

    def test_primitives(self):
        self.assertTrue(isoftype(5, int))
        self.assertFalse(isoftype('hello', int))
        self.assertTrue(isoftype(5, Union[str, int]))
        self.assertFalse(isoftype(True, Union[str, float, type]))
        self.assertTrue(isoftype(5, int))
        self.assertFalse(isoftype(5, float))
        self.assertTrue(isoftype("", str))
        self.assertTrue(isoftype([""], list))
        self.assertTrue(isoftype([""], List[str]))
        self.assertFalse(isoftype([""], List[int]))
        self.assertTrue(isoftype(1, int))
        self.assertTrue(isoftype("hello", str))
        self.assertTrue(isoftype([1, 2, 3], list))
        self.assertTrue(isoftype([1, 2, 3], List[int]))
        self.assertTrue(isoftype({1: "a", 2: "b"}, dict))
        self.assertTrue(isoftype({1: "a", 2: "b"}, Dict[int, str]))
        self.assertFalse(isoftype(1, float))
        self.assertFalse(isoftype("hello", int))
        self.assertFalse(isoftype([1, 2, 3], List[str]))
        self.assertFalse(isoftype([1, 2, "3"], List[int]))
        self.assertFalse(isoftype({1: "a", 2: "b"}, Dict[str, int]))

    def test_advanced_types(self):
        d: Dict[Any, Any] = {}
        d[int] = 0
        d["str"] = str

        self.assertTrue(isoftype("hello", Any))
        self.assertTrue(isoftype([1, 2, "3"], List[Union[int, str]]))
        self.assertTrue(isoftype(Union, type(Union)))
        self.assertTrue(isoftype(Union[int, float], type(Union)))
        self.assertTrue(isoftype(Union, type(Union)))
        self.assertTrue(isoftype(1, Union[int, float]))
        self.assertTrue(isoftype(int, Union[int, float, type]))
        self.assertTrue(isoftype(int, [int, float, type]))
        self.assertTrue(isoftype(1, Union[int, List[int]]))
        self.assertTrue(isoftype([4], Union[int, List[int]]))
        self.assertFalse(isoftype([4.5], Union[int, List[int]]))
        self.assertTrue(isoftype([5, 6], List[int]))
        self.assertTrue(isoftype([5, 6], List[Union[int, float]]))
        self.assertTrue(isoftype([5, 6.3], List[Union[int, float]]))
        self.assertTrue(isoftype([5.0, 6.3], List[Union[int, float]]))
        self.assertTrue(isoftype(dict(one=1), Dict[str, int]))
        self.assertTrue(isoftype(d, Dict[Union[type, str], Any]))
        self.assertTrue(isoftype(d, dict))

    def test_classes(self):
        class MyClass:
            pass

        class MyChildClass(MyClass):
            pass

        class MyOtherClass(MyClass):
            pass

        self.assertTrue(isoftype(MyChildClass(), MyClass))
        self.assertTrue(isoftype(MyChildClass(), MyChildClass))
        self.assertFalse(isoftype(MyChildClass(), MyOtherClass))

    def test_callable(self):
        self.assertFalse(isoftype(lambda x: x + 1, Callable[[int], int]))
        self.assertFalse(isoftype(lambda x: x + 1, Callable[[float], int]))
        self.assertFalse(isoftype(lambda x: x + 1, Callable[[int], Union[int, str]]))
        self.assertFalse(isoftype(lambda x: x + 1, Callable))
        self.assertFalse(isoftype(lambda x: x + 1, Callable[[int], Tuple[int, str]]))
        self.assertTrue(isoftype(lambda x: x + 1, Callable, strict=False))

        def foo(a: int) -> int:
            a += 1
            return a

        self.assertTrue(isoftype(foo, Callable))
        self.assertTrue(isoftype(foo, Callable[[int], int]))
        self.assertTrue(isoftype(Callable, type(Callable)))
        self.assertTrue(isoftype(Callable[[], bool], type(Callable[[], bool])))
        self.assertTrue(isoftype(Callable[[int, float], bool], type(Callable[[int, float], bool])))

    def test_extra(self):
        self.assertTrue(isoftype(1, Union[None, int, str, bool]))
        self.assertFalse(isoftype(1, List[Tuple[str, int]]))
        self.assertFalse(isoftype([1], List[Tuple[str, int]]))
        self.assertFalse(isoftype([(1,)], List[Tuple[str, int]]))
        self.assertTrue(isoftype([("1", 1)], List[Tuple[str, int]]))
        self.assertFalse(isoftype(1, Dict[Union[str, int], Optional[List[float]]]))
        self.assertFalse(isoftype({1: 1}, Dict[Union[str, int], Optional[List[float]]]))
        self.assertTrue(isoftype({1: [1.1], "a": None}, Dict[Union[str, int], Optional[List[float]]]))
        self.assertFalse(isoftype(lambda: 1, Callable[[], int]))
        self.assertTrue(isoftype("1", AnyStr))
        self.assertFalse(isoftype(1, AnyStr))
        self.assertFalse(isoftype(1, Literal["red", "green", "blue"]))
        self.assertTrue(isoftype("red", Literal["red", "green", "blue"]))
        self.assertTrue(isoftype(1, TypeVar("T", int, float, str)))
        self.assertFalse(isoftype((1,), Tuple[str, ...]))
        self.assertFalse(isoftype(1, Iterable[object]))
        self.assertTrue(isoftype([1], Iterable[object]))
        self.assertFalse(isoftype(1, ForwardRef("MyClass")))

        # Test cases for generic types
        self.assertTrue(isoftype([1, 2, 3], List[int]))
        self.assertTrue(isoftype({'a': 1, 'b': 2}, Dict[str, int]))
        self.assertTrue(isoftype((1, 'a'), Optional[Tuple[int, str]]))

        # T = TypeVar("T")
        # # Test cases for type variables
        # assert isoftype(1, int) == True  
        # # True, assuming T is a type variable
        # assert isoftype([1, 2, 3], List[T]) == True
        # assert isoftype([1, 2, 3], List[T | int]) == True
        # assert isoftype([1.2, 2, 3], List[T]) == False
        # # True, assuming T is a type variable
        # assert isoftype({'a': 1, 'b': 2}, Dict[str, T]) == True

        # # Test cases for recursive types
        # # True, assuming T is a type variable
        # assert isoftype([[1, 2], [3, 4]], List[List[T]]) == True
        # # True, assuming T is a type variable
        # assert isoftype({'a': [(1, 2), (3, 4)]},
        #                 Dict[str, List[Tuple[T, T]]]) == True

        # Test cases for variadic types
        self.assertFalse(isoftype((1, 2, 3), Tuple[int, ...]))
        # assert isoftype(1, Union[int, str, ...]))  
        # assert isoftype('a', Union[int, str, ...]))  # True

        # Test cases for union types
        self.assertTrue(isoftype(10, Union[int, str]))
        self.assertTrue(isoftype([1, 2, 3], Union[List[int], List[str]]))
        self.assertTrue(isoftype(['a', 'b', 'c'], Union[List[int], List[str]]))

        # Additional test cases
        self.assertTrue(isoftype(None, Optional[int]))
        self.assertFalse(isoftype(lambda x: x + 1, Callable[[int], int]))

    def test_isoftype_comprehensive_2(self) -> None:
        self.assertTrue(isoftype(5, int))  # Basic type checking
        self.assertTrue(isoftype("Hello", str))
        self.assertFalse(isoftype(5, str))
        self.assertFalse(isoftype("Hello", int))

        self.assertTrue(isoftype(5, Union[int, str]))  # Union type checking
        self.assertTrue(isoftype("Hello", Union[int, str]))
        self.assertFalse(isoftype(5.5, Union[int, str]))
        self.assertTrue(isoftype(True, Union[int, str]))  # TODO

        self.assertTrue(isoftype([1, 2, 3], List[int]))  # Container type checking
        self.assertTrue(isoftype((1, 2, 3), Tuple[int, int, int]))
        self.assertTrue(isoftype({'a': 1, 'b': 2}, Dict[str, int]))
        self.assertFalse(isoftype([1, 2, 3], Tuple[int, int, int]))
        self.assertFalse(isoftype((1, 2, 3), List[int]))
        self.assertFalse(isoftype({'a': 1, 'b': 2}, List[int]))

        def number_generator() -> Generator:
            yield 1
            yield 2
            yield 3

        def string_generator() -> Generator:
            yield "Hello"
            yield "World"

        # Generator type checking
        self.assertTrue(isoftype(number_generator(), Generator[int, None, None]))
        self.assertTrue(isoftype(string_generator(), Generator[str, None, None]))
        # assert not isoftype(number_generator(), Generator[str, None, None])#TODO
        # assert not isoftype(string_generator(), Generator[int, None, None])

        self.assertTrue(isoftype(3, Literal[1, 2, 3]))  # Literal type checking
        self.assertTrue(isoftype("apple", Literal["apple", "banana", "cherry"]))
        self.assertFalse(isoftype(5, Literal[1, 2, 3]))
        self.assertFalse(isoftype("orange", Literal["apple", "banana", "cherry"]))

        T = TypeVar('T', int, str)

        def process_data(data: T) -> T:
            if isoftype(data, int):  # TypeVar and TypeVar constraints
                return data * 2
            elif isoftype(data, str):
                return data.upper()  # type:ignore
            else:
                return data

        self.assertTrue(process_data(5) == 10)
        self.assertTrue(process_data("hello") == "HELLO")
        self.assertTrue(process_data(3.14) == 3.14)  # type:ignore

        def add_numbers(a: int, b: int) -> int:
            return a + b

        def greet(name: str) -> str:
            return "Hello, " + name

        def multiply_numbers(a: int, b: int) -> int:
            return a * b

        # Callable type checking
        self.assertTrue(isoftype(add_numbers, Callable[[int, int], int]))
        self.assertTrue(isoftype(greet, Callable[[str], str]))
        self.assertFalse(isoftype(add_numbers, Callable[[str, str], str]))
        self.assertFalse(isoftype(multiply_numbers, Callable[[int, int], str]))

        # Tree = Union[int, List['Tree']]

        # tree1 = [1, [2, [3], 4], 5]  # Recursive type checking
        # tree2 = [1, [2, [3, [4]]]]
        # tree3 = [1, [2, [3, [4, ['5']]]]]

        # assert isoftype(tree1, Tree)
        # assert isoftype(tree2, Tree)
        # assert not isoftype(tree3, Tree)

        class MyClass:
            pass

        MyType = ForwardRef('MyClass')

        obj = MyClass()

        self.assertTrue(isoftype(obj, MyType))  # ForwardRef type checking
        self.assertFalse(isoftype(obj, ForwardRef('OtherClass')))

    def test_isoftype_comprehensive_3(self):
        # Tree = Union[int, List['Tree']]

        # tree1 = [1, [2, [3, [4, [5, [6]]]]]]
        # tree2 = [1, [2, [3, [4, ['5']]]]]

        # assert isoftype(tree1, Tree)  
        # assert not isoftype(tree2, Tree)  # False

        Myt_dict = Dict[str, Union[List[Tuple[int, str]], str]]

        data1 = {
            "list1": [(1, "one"), (2, "two")],
            "list2": [(3, "three"), (4, "four")],
            "string": "Hello"
        }

        data2 = {
            "list1": [(1, "one"), (2, "two")],
            "list2": [(3, "three"), (4, 4)],
            "string": "Hello"
        }

        self.assertTrue(isoftype(data1, Myt_dict))
        self.assertFalse(isoftype(data2, Myt_dict))  # False

        T1 = TypeVar('T1')
        T2 = TypeVar('T2')

        def process_data(data: List[T1], value: T2) -> List[Tuple[T1, T2]]:
            result = []
            for item in data:
                result.append((item, value))
            return result

        self.assertTrue(isoftype(process_data([1, 2, 3], "A"), List[Tuple[int, str]]))
        self.assertFalse(isoftype(process_data([1, 2, 3], "A"), List[Tuple[str, int]]))  # False

        Person = Tuple[str, Union[int, List[Dict[str, Union[str, int]]]]]

        data1_ = ("John", 30)
        data2_ = ("Alice", [{"name": "Bob", "age": 25},
                            {"name": "Carol", "age": 35}])
        data3_ = ("Tom", [{"name": "Jerry", "age": "twenty"},
                          {"name": "Spike", "age": 5}])

        self.assertTrue(isoftype(data1_, Person))
        self.assertTrue(isoftype(data2_, Person))
        self.assertTrue(isoftype(data3_, Person))

    def test_protocol1(self):
        T = TypeVar('T')

        @runtime_checkable
        class Fooable(Protocol):
            def foo(self): ...

        @runtime_checkable
        class Barable(Protocol[T]):
            def bar(self) -> T: ...

        class A:
            def foo(self): ...

        class B:
            def bar(self) -> int: ...  # type:ignore

        self.assertTrue(isoftype(A, Fooable))
        self.assertFalse(isoftype(A, Barable))
        self.assertFalse(isoftype(B, Fooable))
        self.assertTrue(isoftype(B, Barable))
        self.assertFalse(isoftype(B, Barable[int]))
        self.assertFalse(isoftype(B, Barable[float]))
        self.assertTrue(isoftype(B, Type[Barable[int]]))
        self.assertFalse(isoftype(B, Type[Barable[float]]))

    def test_protocol2(self):
        class A(JavaInterface):
            def foo(self): ...

        class B(A):
            def foo(self):
                pass

        self.assertTrue(isoftype(A, Protocol))
        self.assertTrue(issubclass(B, A))
        self.assertFalse(isoftype(B, A))
        self.assertTrue(isoftype(B(), A))

        class B:
            def foo(self):
                pass

        self.assertFalse(isoftype(B, A))
        self.assertTrue(isoftype(B(), A))

    def test_protocol3(self):
        T = TypeVar('T')

        class A(Protocol, Generic[T]):
            def foo(self, a: T) -> None: ...

        class B:
            def foo(self, a: float) -> None:
                pass


        self.assertFalse(isoftype(B, A[int]))
        self.assertFalse(isoftype(B(), A[int]))
        self.assertTrue(isoftype(B(), A[float]))
        self.assertTrue(isoftype(B(), A[Union[int, float]]))
