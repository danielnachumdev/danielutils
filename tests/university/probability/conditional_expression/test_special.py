import unittest
from danielutils import Geo as G

X = G(0.5)


class TestSpecial(unittest.TestCase):
    def test_multiple_inequillities(self):
        a = 0 < X < 2
        b = (0 < X) < 2
        c = 0 < X and X < 2
        self.assertEqual(0 < X < 2, 0 < X & X < 2)
        self.assertEqual(0 < X < 2, (0 < X) < 2)
        self.assertEqual(0 < X < 2, 0 < (X < 2))
