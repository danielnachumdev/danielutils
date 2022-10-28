from ..danielutils import TestFactory, Test
from ..danielutils.Decorators import *


def test_validate():
    assert TestFactory(validate).add_tests([

    ])()


def test_NotImplemented():
    assert TestFactory(NotImplemented).add_tests([

    ])()


def test_PartiallyImplemented():
    assert TestFactory(PartiallyImplemented).add_tests([

    ])()


def test_memo():
    assert TestFactory(memo).add_tests([

    ])()


def test_overload():
    assert TestFactory(overload).add_tests([

    ])()


def test_abstractmethod():
    assert TestFactory(abstractmethod).add_tests([

    ])()


def test_deprecate():
    assert TestFactory(deprecate).add_tests([

    ])()


def test_atomic():
    assert TestFactory(atomic).add_tests([

    ])()


def test_limit_recursion():
    assert TestFactory(limit_recursion).add_tests([

    ])()
