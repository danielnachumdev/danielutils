from ..danielutils.Testing import TestFactory, Test
from ..danielutils.Typing import *


def test_isoftype():
    d = dict()
    d[int] = 0
    d["str"] = str

    def foo(a: int) -> int:
        pass

    class MyClass:
        pass

    class MyChildClass(MyClass):
        pass

    class MyOtherClass(MyClass):
        pass

    assert TestFactory(isoftype).add_tests([
        Test((5, int), True),
        Test((5, float), False),
        Test(([5, 6], list[int]), True),
        Test(([5, 6], list[Union[int, float]]), True),
        Test(([5, 6.3], list[Union[int, float]]), True),
        Test(([5.0, 6.3], list[Union[int, float]]), True),
        Test((dict(one=1), dict[str, int]), True),
        Test((d, dict[Union[type, str], Any]), True),
        Test((d, dict), True),
        Test(("", str), True),
        Test(([""], list), True),
        Test(([""], list[str]), True),
        Test(([""], list[int]), False),
        Test((1, Union[int, float]), True),
        Test((int, Union[int, float, type]), True),
        Test((int, [int, float, type]), True),
        Test((1, Union[int, list[int]]), True),
        Test(([4], Union[int, list[int]]), True),
        Test(([4.5], Union[int, list[int]]), False),
        Test((Union, type(Union)), True),
        Test((Union[int, float], type(Union)), True),
        Test((Callable, type(Callable)), True),
        Test((Callable[[], bool], type(Callable)), True),
        Test((Callable[[], bool], type(Callable[[], bool])), True),
        Test((Callable[[int, float], bool], type(
            Callable[[int, float], bool])), True),
        Test((foo, Callable), True),
        Test((foo, Callable[[int], int]), True),
        Test((Union, type(Union)), True),
        Test((1, int), True),
        Test(("hello", str), True),
        Test(([1, 2, 3], list), True),
        Test(([1, 2, 3], list[int]), True),
        Test(([1, 2, "3"], list[Union[int, str]]), True),
        Test(({1: "a", 2: "b"}, dict), True),
        Test(({1: "a", 2: "b"}, dict[int, str]), True),
        Test((1, float), False),
        Test(("hello", int), False),
        Test(([1, 2, 3], list[str]), False),
        Test(([1, 2, "3"], list[int]), False),
        Test(({1: "a", 2: "b"}, dict[str, int]), False),
        Test((lambda x: x+1, Callable[[int], int]), True),
        Test((lambda x: x+1, Callable[[float], int]), False),
        Test((lambda x: x+1, Callable[[int], Union[int, str]]), True),
        Test((lambda x: x+1, Callable[[int], tuple[int, str]]), False),
        Test((MyClass(), MyClass), True),
        Test((MyChildClass(), MyClass), True),
        Test((MyChildClass(), MyChildClass), True),
        Test((MyChildClass(), MyOtherClass), False),
        Test(("hello", Any), True),
    ])()
