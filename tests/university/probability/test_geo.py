import unittest

from danielutils import Geo as G, ProbabilityFunction as P


class TestGeo(unittest.TestCase):
    def test_simple(self):
        X = G(0.5)
        self.assertEqual(0.25, P(X == 1))
        self.assertEqual(0.25, P(X == 2 | X > 1))
