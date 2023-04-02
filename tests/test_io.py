from ..danielutils import TestFactory, Test
from ..danielutils.IO import *


def test_write_to_file():
    assert TestFactory(write_to_file).add_tests([

    ])()


def test_file_exists():
    assert TestFactory(file_exists).add_tests([

    ])()


def test_delete_file():
    assert TestFactory(delete_file).add_tests([

    ])()


def test_read_file():
    assert TestFactory(read_file).add_tests([

    ])()


def test_is_file():
    assert TestFactory(is_file).add_tests([

    ])()


def test_is_directory():
    assert TestFactory(is_directory).add_tests([

    ])()


def test_get_files():
    assert TestFactory(get_files).add_tests([

    ])()


def test_get_files_and_directories():
    assert TestFactory(get_files_and_directories).add_tests([

    ])()


def test_get_directories():
    assert TestFactory(get_directories).add_tests([

    ])()


def test_delete_directory():
    assert TestFactory(delete_directory).add_tests([

    ])()


def test_get_file_type_from_directory():
    assert TestFactory(get_file_type_from_directory).add_tests([

    ])()


def test_get_file_type_from_directory_recursively():
    assert TestFactory(get_file_type_from_directory_recursively).add_tests([

    ])()
