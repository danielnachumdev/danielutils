from ..danielutils import TestFactory, Test
from ..danielutils.Testing import *


def test___init__():
    assert TestFactory(Test.__init__).add_tests([

    ])()


def test___init__():
    assert TestFactory(TestFactory.__init__).add_tests([

    ])()


def test_add_test():
    assert TestFactory(TestFactory.add_test).add_tests([

    ])()


def test_add_tests():
    assert TestFactory(TestFactory.add_tests).add_tests([

    ])()


def test___call__():
    assert TestFactory(TestFactory.__call__).add_tests([

    ])()


def test_create_test_file():
    assert TestFactory(create_test_file).add_tests([

    ])()
