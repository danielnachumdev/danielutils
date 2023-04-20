from ...danielutils.Functions import isoftype
from typing import *


def test_primitives():
    assert isoftype(5, int) == True
    assert isoftype('hello', int) == False
    assert isoftype(5, Union[str, int]) == True
    assert isoftype(True, Union[str, float, type]) == False
    assert isoftype(5, int) == True
    assert isoftype(5, float) == False
    assert isoftype("", str) == True
    assert isoftype([""], list) == True
    assert isoftype([""], list[str]) == True
    assert isoftype([""], list[int]) == False
    assert isoftype(1, int) == True
    assert isoftype("hello", str) == True
    assert isoftype([1, 2, 3], list) == True
    assert isoftype([1, 2, 3], list[int]) == True
    assert isoftype({1: "a", 2: "b"}, dict) == True
    assert isoftype({1: "a", 2: "b"}, dict[int, str]) == True
    assert isoftype(1, float) == False
    assert isoftype("hello", int) == False
    assert isoftype([1, 2, 3], list[str]) == False
    assert isoftype([1, 2, "3"], list[int]) == False
    assert isoftype({1: "a", 2: "b"}, dict[str, int]) == False


def test_advanced_types():
    d = {}
    d[int] = 0
    d["str"] = str

    assert isoftype("hello", Any) == True
    assert isoftype([1, 2, "3"], list[Union[int, str]]) == True
    assert isoftype(Union, type(Union)) == True
    assert isoftype(Union[int, float], type(Union)) == True
    assert isoftype(Union, type(Union)) == True
    assert isoftype(1, Union[int, float]) == True
    assert isoftype(int, Union[int, float, type]) == True
    assert isoftype(int, [int, float, type]) == True
    assert isoftype(1, Union[int, list[int]]) == True
    assert isoftype([4], Union[int, list[int]]) == True
    assert isoftype([4.5], Union[int, list[int]]) == False
    assert isoftype([5, 6], list[int]) == True
    assert isoftype([5, 6], list[Union[int, float]]) == True
    assert isoftype([5, 6.3], list[Union[int, float]]) == True
    assert isoftype([5.0, 6.3], list[Union[int, float]]) == True
    assert isoftype(dict(one=1), dict[str, int]) == True
    assert isoftype(d, dict[Union[type, str], Any]) == True
    assert isoftype(d, dict) == True


def test_classes():
    class MyClass:
        pass

    class MyChildClass(MyClass):
        pass

    class MyOtherClass(MyClass):
        pass

    assert isoftype(MyChildClass(), MyClass) == True
    assert isoftype(MyChildClass(), MyChildClass) == True
    assert isoftype(MyChildClass(), MyOtherClass) == False


def test_callable():
    assert isoftype(lambda x: x+1, Callable[[int], int]) == False
    assert isoftype(lambda x: x+1, Callable[[float], int]) == False
    assert isoftype(lambda x: x+1, Callable[[int], Union[int, str]]) == False
    assert isoftype(lambda x: x+1, Callable) == False
    assert isoftype(lambda x: x+1, Callable[[int], tuple[int, str]]) == False
    assert isoftype(lambda x: x+1, Callable, strict=False) == True

    def foo(a: int) -> int:
        a += 1
    assert isoftype(foo, Callable) == True
    assert isoftype(foo, Callable[[int], int]) == True
    assert isoftype(Callable, type(Callable)) == True
    assert isoftype(Callable[[], bool], type(Callable[[], bool])) == True
    assert isoftype(Callable[[int, float], bool], type(
        Callable[[int, float], bool])) == True
