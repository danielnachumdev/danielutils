import unittest
from danielutils import MockImportObject


class TestMockImportObject(unittest.TestCase):
    def test__getattr__(self):
        some_module = MockImportObject("`some_module` is not installed")
        with self.assertRaises(ImportError):
            some_module.anything

    def test__init__(self):
        some_class = MockImportObject("`some_module` is not installed")
        with self.assertRaises(ImportError):
            some_class(1, 2, 3, 4, asd=12476)
