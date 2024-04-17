import unittest
from danielutils.university.probability import Geometric as G

X = G(0.5)


class TestSpecial(unittest.TestCase):
    def test_multiple_inequillities(self):
        self.assertEqual((0 < X) < 2, (0 < X) & (X < 2))
        self.assertEqual((0 < X) < 2, (0 < X) < 2)
        self.assertEqual((0 < X) < 2, 0 < (X < 2))
