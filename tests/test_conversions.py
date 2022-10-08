from ..danielutils import TestFactory, Test
from ..danielutils.Conversions import *


def test_char_to_int():
    assert TestFactory(char_to_int).add_tests([
        Test('a', 97),
        Test('א', 1488)
    ])()


def test_int_to_char():
    assert TestFactory(int_to_char).add_tests([

    ])()


def test_hex_to_char():
    assert TestFactory(hex_to_char).add_tests([

    ])()


def test_hex_to_dec():
    assert TestFactory(hex_to_dec).add_tests([

    ])()


def test_char_to_hex():
    assert TestFactory(char_to_hex).add_tests([

    ])()


def test_dec_to_hex():
    assert TestFactory(dec_to_hex).add_tests([

    ])()


def test_int_to_hex():
    assert TestFactory(int_to_hex).add_tests([

    ])()


def test_to_hex():
    assert TestFactory(to_hex).add_tests([
        Test(97, "0x61"),
        Test('a', "0x61"),
    ])()
