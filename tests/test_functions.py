from ..danielutils.Testing import TestFactory, Test
from ..danielutils.Functions import *
from ..danielutils.Typing import Union, Any, Callable


def test_isoftype():
    d = dict()
    d[int] = 0
    d["str"] = str

    def foo(a: int) -> int:
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
        # Test((Union, type(Union)), True),
    ])()


class A:
    def __init__(self):
        pass


class B(A):
    def __init__(self):
        pass


def test_isoneof():
    assert TestFactory(isoneof).add_tests([
        Test((5, [int]), True),
        Test((6.5, [int]), False),
        Test((5, [Union[int, float]]), True),
        Test(([5, 5.5], [list]), True),
        Test(([5, 5.5], [list[Union[int, float]]]), True),
        Test(([5, 5.5], [list[int]]), False),
        Test(([5, 5.5], [list[float]]), False),
        Test((tuple(), [tuple]), True),
        Test((Test(1, 1), [Test]), True),
        Test((Test(1, 1), [Test]), True),
        Test((B(), [A]), True)
    ])()


def test_isoneof_strict():
    assert TestFactory(isoneof_strict).add_tests([
        Test((5, [int]), True),
        Test((5, [float]), False),
        Test((B(), [A]), False)
    ])()


def test_areoneof():
    assert TestFactory(areoneof).add_tests([
        Test(([6, 6.6], [int, float]), True),
        Test(([[5], [5.5]], [list[int], list[float]]), True),
        Test(([], []), True),
    ])()


def test_check_foreach():
    from ..danielutils.Text import is_number
    assert TestFactory(check_foreach).add_tests([
        Test(("1213459", is_number), True),
        Test(("12134a59", is_number), False)
    ])()
