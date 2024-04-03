
import random
import unittest
from typing import Union, Any, List as t_list, Tuple as t_tuple
from danielutils.classes.typed_builtins import tlist  # type:ignore
from danielutils import isoftype  # type:ignore
from danielutils.reflection import get_python_version  # type:ignore

if get_python_version() >= (3, 9):
    from builtins import list as t_list, tuple as t_tuple  # type:ignore


class TestTlist(unittest.TestCase):

    def test_basic(self):
        with self.assertRaises(ValueError):
            tlist(1)

        tlist[int]()
        tlist[float]()
        tlist[Union[int, float]]()
        tlist[Union[int, float]]()
        tlist[Any]()

    def test_correct_values(self):
        tlist[int]([1, 2, 3, 4])
        tlist[float]([0.1, 0.1, 0.2])
        tlist[Union[int, float]]([1, 2, 3, 0.1, 0.2])
        tlist[Union[int, float]]([1, 23, 3, 0.1, 0.2])
        tlist[Any]([1, 2, 0.2, 0.63, [], [1]])

    def test_wrong_values(self):
        with self.assertRaises(ValueError):
            tlist[float]([1, 2, 3, 4])
        with self.assertRaises(ValueError):
            tlist[int]([1, 2, 3, "4"])
        with self.assertRaises(ValueError):
            tlist[Union[int, float]]([1, 2.2, 3, "4"])
        with self.assertRaises(ValueError):
            tlist[t_tuple[int]]([[1], [2], [3], ["4"]])

    def test_isinstance(self):
        self.assertTrue(isinstance([1, 2, 3, 4], tlist[int]))
        self.assertTrue(isinstance([0.1, 0.1, 0.2], tlist[float]))
        self.assertTrue(isinstance([1, 2, 3, 0.1, 0.2], tlist[Union[int, float]]))
        self.assertTrue(isinstance([1, 23, 3, 0.1, 0.2], tlist[Union[int, float]]))
        self.assertTrue(isinstance([1, 2, 0.2, 0.63, [], [1]], tlist[Any]))

    def test_isinstanse_fail(self):
        self.assertFalse(isinstance([1, 2, 3, "4"], tlist[int]))
        self.assertFalse(isinstance([0.1, 0.1, " 0.2"], tlist[float]))
        self.assertFalse(isinstance([1, 2, 3, 0.1, "0.2"], tlist[Union[int, float]]))
        self.assertFalse(isinstance([1, 23, 3, 0.1, " 0.2"], tlist[Union[int, float]]))

    def test_isinstance_with_regular_list(self):
        a = tlist[int]([1, 2, 3])
        self.assertTrue(isinstance(a, list))
        self.assertTrue(isoftype(a, t_list[int]))
        self.assertTrue(isoftype(a, t_list[Union[int, float]]))

    def test_extend(self):
        for _ in range(100):
            l = []
            for __ in range(10):
                l.append(random.randint(0, 100))

            a = tlist[int](l)

            # test copy constructor
            b = tlist[int](a)

            a.extend(b)

            # check addition, multiplication and equality
            self.assertEqual(a, b + b)
            self.assertEqual(b + b, b * 2)
