from typing import *
from ...danielutils.Functions import isoftype


def test_primitives():
    assert isoftype(5, int) is True
    assert isoftype('hello', int) is False
    assert isoftype(5, Union[str, int]) is True
    assert isoftype(True, Union[str, float, type]) is False
    assert isoftype(5, int) is True
    assert isoftype(5, float) is False
    assert isoftype("", str) is True
    assert isoftype([""], list) is True
    assert isoftype([""], list[str]) is True
    assert isoftype([""], list[int]) is False
    assert isoftype(1, int) is True
    assert isoftype("hello", str) is True
    assert isoftype([1, 2, 3], list) is True
    assert isoftype([1, 2, 3], list[int]) is True
    assert isoftype({1: "a", 2: "b"}, dict) is True
    assert isoftype({1: "a", 2: "b"}, dict[int, str]) is True
    assert isoftype(1, float) is False
    assert isoftype("hello", int) is False
    assert isoftype([1, 2, 3], list[str]) is False
    assert isoftype([1, 2, "3"], list[int]) is False
    assert isoftype({1: "a", 2: "b"}, dict[str, int]) is False


def test_advanced_types():
    d = {}
    d[int] = 0
    d["str"] = str

    assert isoftype("hello", Any) is True
    assert isoftype([1, 2, "3"], list[Union[int, str]]) is True
    assert isoftype(Union, type(Union)) is True
    assert isoftype(Union[int, float], type(Union)) is True
    assert isoftype(Union, type(Union)) is True
    assert isoftype(1, Union[int, float]) is True
    assert isoftype(int, Union[int, float, type]) is True
    assert isoftype(int, [int, float, type]) is True
    assert isoftype(1, Union[int, list[int]]) is True
    assert isoftype([4], Union[int, list[int]]) is True
    assert isoftype([4.5], Union[int, list[int]]) is False
    assert isoftype([5, 6], list[int]) is True
    assert isoftype([5, 6], list[Union[int, float]]) is True
    assert isoftype([5, 6.3], list[Union[int, float]]) is True
    assert isoftype([5.0, 6.3], list[Union[int, float]]) is True
    assert isoftype(dict(one=1), dict[str, int]) is True
    assert isoftype(d, dict[Union[type, str], Any]) is True
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
    assert isoftype(lambda x: x+1, Callable[[int], tuple[int, str]]) is False
    assert isoftype(lambda x: x+1, Callable, strict=False) is True

    def foo(a: int) -> int:
        a += 1
    assert isoftype(foo, Callable) is True
    assert isoftype(foo, Callable[[int], int]) is True
    assert isoftype(Callable, type(Callable)) is True
    assert isoftype(Callable[[], bool], type(Callable[[], bool])) is True
    assert isoftype(Callable[[int, float], bool], type(
        Callable[[int, float], bool])) is True


def test_extra():
    assert isoftype(1, Union[None, int, str, bool]) == True
    assert isoftype(1, List[Tuple[str, int]]) == False
    assert isoftype([1], List[Tuple[str, int]]) == False
    assert isoftype([(1,)], List[Tuple[str, int]]) == False
    assert isoftype([("1", 1)], List[Tuple[str, int]]) == True
    assert isoftype(1, Dict[Union[str, int], Optional[List[float]]]) == False
    assert isoftype({1: 1}, Dict[Union[str, int],
                    Optional[List[float]]]) == False
    assert isoftype({1: [1.1], "a": None},
                    Dict[Union[str, int], Optional[List[float]]]) == True
    assert isoftype(lambda: 1, Callable[[], int]) == False
    assert isoftype("1", AnyStr) == True
    assert isoftype(1, AnyStr) == False
    assert isoftype(1, Literal["red", "green", "blue"]) == False
    assert isoftype("red", Literal["red", "green", "blue"]) == True
    assert isoftype(1, TypeVar("T", int, float, str)) == True
    assert isoftype((1,), Tuple[str, ...]) == False
    assert isoftype(1, Iterable[object]) == False
    assert isoftype([1], Iterable[object]) == True
    assert isoftype(1, ForwardRef("MyClass")) == False

    # Test cases for generic types
    assert isoftype([1, 2, 3], List[int]) == True  # True
    assert isoftype({'a': 1, 'b': 2}, Dict[str, int]) == True  # True
    assert isoftype((1, 'a'), Optional[Tuple[int, str]]) == True  # True

    T = TypeVar("T")
    # Test cases for type variables
    assert isoftype(1, int) == True  # True
    # True, assuming T is a type variable
    assert isoftype([1, 2, 3], List[T]) == True
    assert isoftype([1, 2, 3], List[T | int]) == True
    assert isoftype([1.2, 2, 3], List[T]) == False
    # True, assuming T is a type variable
    assert isoftype({'a': 1, 'b': 2}, Dict[str, T]) == True

    # Test cases for recursive types
    # True, assuming T is a type variable
    assert isoftype([[1, 2], [3, 4]], List[List[T]]) == True
    # True, assuming T is a type variable
    assert isoftype({'a': [(1, 2), (3, 4)]},
                    Dict[str, List[Tuple[T, T]]]) == True

    # Test cases for variadic types
    assert isoftype((1, 2, 3), Tuple[int, ...]) == False  # True
    # assert isoftype(1, Union[int, str, ...]))  # True
    # assert isoftype('a', Union[int, str, ...]))  # True

    # Test cases for union types
    assert isoftype(10, Union[int, str]) == True  # True
    assert isoftype([1, 2, 3], Union[List[int], List[str]]) == True  # True
    assert isoftype(['a', 'b', 'c'], Union[List[int],
                    List[str]]) == True  # True

    # Additional test cases
    assert isoftype(None, Optional[int]) == True  # True
    assert isoftype(lambda x: x + 1, Callable[[int], int]) == False  # True
