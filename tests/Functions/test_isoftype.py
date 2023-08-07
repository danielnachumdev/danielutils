from typing import Union, Callable, Any, Optional, TypeVar, Iterable, ForwardRef, Literal,\
    AnyStr, Generator, List as t_list, Dict as t_dict, Tuple as t_tuple
from ...danielutils.Functions import isoftype  # type:ignore
from ...danielutils.Reflection import get_python_version  # type:ignore
if get_python_version() >= (3, 9):
    from builtins import list as t_list, dict as t_dict, tuple as t_tuple  # type:ignore


def test_primitives():
    assert isoftype(5, int) is True
    assert isoftype('hello', int) is False
    assert isoftype(5, Union[str, int]) is True
    assert isoftype(True, Union[str, float, type]) is False
    assert isoftype(5, int) is True
    assert isoftype(5, float) is False
    assert isoftype("", str) is True
    assert isoftype([""], list) is True
    assert isoftype([""], t_list[str]) is True
    assert isoftype([""], t_list[int]) is False
    assert isoftype(1, int) is True
    assert isoftype("hello", str) is True
    assert isoftype([1, 2, 3], list) is True
    assert isoftype([1, 2, 3], t_list[int]) is True
    assert isoftype({1: "a", 2: "b"}, dict) is True
    assert isoftype({1: "a", 2: "b"}, t_dict[int, str]) is True
    assert isoftype(1, float) is False
    assert isoftype("hello", int) is False
    assert isoftype([1, 2, 3], t_list[str]) is False
    assert isoftype([1, 2, "3"], t_list[int]) is False
    assert isoftype({1: "a", 2: "b"}, t_dict[str, int]) is False


def test_advanced_types():
    d: t_dict[Any, Any] = {}
    d[int] = 0
    d["str"] = str

    assert isoftype("hello", Any) is True
    assert isoftype([1, 2, "3"], t_list[Union[int, str]]) is True
    assert isoftype(Union, type(Union)) is True
    assert isoftype(Union[int, float], type(Union)) is True
    assert isoftype(Union, type(Union)) is True
    assert isoftype(1, Union[int, float]) is True
    assert isoftype(int, Union[int, float, type]) is True
    assert isoftype(int, [int, float, type]) is True
    assert isoftype(1, Union[int, t_list[int]]) is True
    assert isoftype([4], Union[int, t_list[int]]) is True
    assert isoftype([4.5], Union[int, t_list[int]]) is False
    assert isoftype([5, 6], t_list[int]) is True
    assert isoftype([5, 6], t_list[Union[int, float]]) is True
    assert isoftype([5, 6.3], t_list[Union[int, float]]) is True
    assert isoftype([5.0, 6.3], t_list[Union[int, float]]) is True
    assert isoftype(dict(one=1), t_dict[str, int]) is True
    assert isoftype(d, t_dict[Union[type, str], Any]) is True
    assert isoftype(d, dict) is True


def test_classes():
    class MyClass:
        pass

    class MyChildClass(MyClass):
        pass

    class MyOtherClass(MyClass):
        pass

    assert isoftype(MyChildClass(), MyClass) is True
    assert isoftype(MyChildClass(), MyChildClass) is True
    assert isoftype(MyChildClass(), MyOtherClass) is False


def test_callable():
    assert isoftype(lambda x: x+1, Callable[[int], int]) is False
    assert isoftype(lambda x: x+1, Callable[[float], int]) is False
    assert isoftype(lambda x: x+1, Callable[[int], Union[int, str]]) is False
    assert isoftype(lambda x: x+1, Callable) is False
    assert isoftype(lambda x: x+1, Callable[[int], t_tuple[int, str]]) is False
    assert isoftype(lambda x: x+1, Callable, strict=False) is True

    def foo(a: int) -> int:
        a += 1
        return a

    assert isoftype(foo, Callable) is True
    assert isoftype(foo, Callable[[int], int]) is True
    assert isoftype(Callable, type(Callable)) is True
    assert isoftype(Callable[[], bool], type(Callable[[], bool])) is True
    assert isoftype(Callable[[int, float], bool], type(
        Callable[[int, float], bool])) is True


def test_extra():
    assert isoftype(1, Union[None, int, str, bool]) == True
    assert isoftype(1, t_list[t_tuple[str, int]]) == False
    assert isoftype([1], t_list[t_tuple[str, int]]) == False
    assert isoftype([(1,)], t_list[t_tuple[str, int]]) == False
    assert isoftype([("1", 1)], t_list[t_tuple[str, int]]) == True
    assert isoftype(1, t_dict[Union[str, int],
                    Optional[t_list[float]]]) == False
    assert isoftype({1: 1}, t_dict[Union[str, int],
                    Optional[t_list[float]]]) == False
    assert isoftype({1: [1.1], "a": None},
                    t_dict[Union[str, int], Optional[t_list[float]]]) == True
    assert isoftype(lambda: 1, Callable[[], int]) == False
    assert isoftype("1", AnyStr) == True
    assert isoftype(1, AnyStr) == False
    assert isoftype(1, Literal["red", "green", "blue"]) == False
    assert isoftype("red", Literal["red", "green", "blue"]) == True
    assert isoftype(1, TypeVar("T", int, float, str)) == True
    assert isoftype((1,), t_tuple[str, ...]) == False
    assert isoftype(1, Iterable[object]) == False
    assert isoftype([1], Iterable[object]) == True
    assert isoftype(1, ForwardRef("MyClass")) == False

    # Test cases for generic types
    assert isoftype([1, 2, 3], t_list[int]) == True  # True
    assert isoftype({'a': 1, 'b': 2}, t_dict[str, int]) == True  # True
    assert isoftype((1, 'a'), Optional[t_tuple[int, str]]) == True  # True

    # T = TypeVar("T")
    # # Test cases for type variables
    # assert isoftype(1, int) == True  # True
    # # True, assuming T is a type variable
    # assert isoftype([1, 2, 3], t_list[T]) == True
    # assert isoftype([1, 2, 3], t_list[T | int]) == True
    # assert isoftype([1.2, 2, 3], t_list[T]) == False
    # # True, assuming T is a type variable
    # assert isoftype({'a': 1, 'b': 2}, t_dict[str, T]) == True

    # # Test cases for recursive types
    # # True, assuming T is a type variable
    # assert isoftype([[1, 2], [3, 4]], t_list[t_list[T]]) == True
    # # True, assuming T is a type variable
    # assert isoftype({'a': [(1, 2), (3, 4)]},
    #                 t_dict[str, t_list[t_tuple[T, T]]]) == True

    # Test cases for variadic types
    assert isoftype((1, 2, 3), t_tuple[int, ...]) == False  # True
    # assert isoftype(1, Union[int, str, ...]))  # True
    # assert isoftype('a', Union[int, str, ...]))  # True

    # Test cases for union types
    assert isoftype(10, Union[int, str]) == True  # True
    assert isoftype([1, 2, 3], Union[t_list[int], t_list[str]]) == True  # True
    assert isoftype(['a', 'b', 'c'], Union[t_list[int],
                    t_list[str]]) == True  # True

    # Additional test cases
    assert isoftype(None, Optional[int]) == True  # True
    assert isoftype(lambda x: x + 1, Callable[[int], int]) == False  # True


def test_isoftype_comprehensive_2() -> None:
    assert isoftype(5, int)  # Basic type checking
    assert isoftype("Hello", str)
    assert not isoftype(5, str)
    assert not isoftype("Hello", int)

    assert isoftype(5, Union[int, str])  # Union type checking
    assert isoftype("Hello", Union[int, str])
    assert not isoftype(5.5, Union[int, str])
    assert isoftype(True, Union[int, str])  # TODO

    assert isoftype([1, 2, 3], t_list[int])  # Container type checking
    assert isoftype((1, 2, 3), t_tuple[int, int, int])
    assert isoftype({'a': 1, 'b': 2}, t_dict[str, int])
    assert not isoftype([1, 2, 3], t_tuple[int, int, int])
    assert not isoftype((1, 2, 3), t_list[int])
    assert not isoftype({'a': 1, 'b': 2}, t_list[int])

    def number_generator() -> Generator:
        yield 1
        yield 2
        yield 3

    def string_generator() -> Generator:
        yield "Hello"
        yield "World"

    # Generator type checking
    assert isoftype(number_generator(), Generator[int, None, None])
    assert isoftype(string_generator(), Generator[str, None, None])
    # assert not isoftype(number_generator(), Generator[str, None, None])#TODO
    # assert not isoftype(string_generator(), Generator[int, None, None])

    assert isoftype(3, Literal[1, 2, 3])  # Literal type checking
    assert isoftype("apple", Literal["apple", "banana", "cherry"])
    assert not isoftype(5, Literal[1, 2, 3])
    assert not isoftype("orange", Literal["apple", "banana", "cherry"])

    T = TypeVar('T', int, str)

    def process_data(data: T) -> T:
        if isoftype(data, int):  # TypeVar and TypeVar constraints
            return data * 2
        elif isoftype(data, str):
            return data.upper()  # type:ignore
        else:
            return data

    assert process_data(5) == 10
    assert process_data("hello") == "HELLO"
    assert process_data(3.14) == 3.14  # type:ignore

    def add_numbers(a: int, b: int) -> int:
        return a + b

    def greet(name: str) -> str:
        return "Hello, " + name

    def multiply_numbers(a: int, b: int) -> int:
        return a * b

    # Callable type checking
    assert isoftype(add_numbers, Callable[[int, int], int])
    assert isoftype(greet, Callable[[str], str])
    assert not isoftype(add_numbers, Callable[[str, str], str])
    assert not isoftype(multiply_numbers, Callable[[int, int], str])

    # Tree = Union[int, t_list['Tree']]

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

    assert isoftype(obj, MyType)  # ForwardRef type checking
    assert not isoftype(obj, ForwardRef('OtherClass'))


def test_isoftype_comprehensive_3():
    # Tree = Union[int, t_list['Tree']]

    # tree1 = [1, [2, [3, [4, [5, [6]]]]]]
    # tree2 = [1, [2, [3, [4, ['5']]]]]

    # assert isoftype(tree1, Tree)  # True
    # assert not isoftype(tree2, Tree)  # False

    Myt_dict = t_dict[str, Union[t_list[t_tuple[int, str]], str]]

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

    assert isoftype(data1, Myt_dict)  # True
    assert not isoftype(data2, Myt_dict)  # False

    T1 = TypeVar('T1')
    T2 = TypeVar('T2')

    def process_data(data: t_list[T1], value: T2) -> t_list[t_tuple[T1, T2]]:
        result = []
        for item in data:
            result.append((item, value))
        return result

    assert isoftype(process_data([1, 2, 3], "A"),
                    t_list[t_tuple[int, str]])  # True
    assert not isoftype(process_data(
        [1, 2, 3], "A"), t_list[t_tuple[str, int]])  # False

    Person = t_tuple[str, Union[int, t_list[t_dict[str, Union[str, int]]]]]

    data1_ = ("John", 30)
    data2_ = ("Alice", [{"name": "Bob", "age": 25},
                        {"name": "Carol", "age": 35}])
    data3_ = ("Tom", [{"name": "Jerry", "age": "twenty"},
                      {"name": "Spike", "age": 5}])

    assert isoftype(data1_, Person)  # True
    assert isoftype(data2_, Person)  # True
    assert isoftype(data3_, Person)  # True
