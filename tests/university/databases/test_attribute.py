import functools
import unittest

from danielutils import Attribute  # type:ignore


class TestAttribute(unittest.TestCase):

    def test_init(self):
        Attribute()
        Attribute("")
        Attribute("A")
        Attribute("A")
        Attribute("A")
        Attribute("a")

    def test_equallity(self):
        A = Attribute()
        B = Attribute()
        self.assertEqual(A, B)
        C, D = Attribute("A"), Attribute("A")
        self.assertEqual(C, D)
        self.assertNotEqual(A, C)
        self.assertTrue(A is not B)
        self.assertTrue(A is not A.clone())
        self.assertEqual(A, A.clone())
        self.assertEqual(hash(A), hash(A.clone()))
        self.assertEqual(Attribute("ABCDE"), Attribute("ABCDE"[::-1]))
        self.assertEqual(hash(Attribute("ABCDE")), hash(Attribute("ABCDE"[::-1])))

    def test_1(self):
        ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for i in range(1, len(ABC)):
            attributes = Attribute.create_many(i)
            X = functools.reduce(
                lambda prev, curr: prev.union(curr),
                attributes,
            )
            Y = functools.reduce(
                lambda prev, curr: prev + curr,
                attributes,
            )
            self.assertEqual(X, Attribute(ABC[:i]))
            self.assertEqual(Attribute(ABC[:i]), Y)
            self.assertEqual(Attribute(), X - Y)
