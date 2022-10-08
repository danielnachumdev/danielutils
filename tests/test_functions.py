from ..danielutils.Testing import TestFactory, Test
from ..danielutils.Functions import *
from typing import Union, Any


def test_isoftype():
    d = dict()
    d[int] = 0
    d["str"] = str

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
