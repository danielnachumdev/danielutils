import unittest

from danielutils.university.probability import Geometric as G, probability_function as P

X = G(0.5)


class TestGeo(unittest.TestCase):
    def test_equality(self):
        self.assertEqual(0.5, P(X == 1))
        self.assertEqual(P(X == 1), P(X == 1))

    def test_not_equal(self):
        self.assertEqual(1 - P(X != 1), P(X == 1))

    def test_inequality(self):
        self.assertEqual(1 - P(X <= 1), P(X > 1))

    def test_and(self):
        self.assertEqual(P((X > 0) & (X > 0)), P(X > 0))
        self.assertEqual(P((0 < X) < 2), P(X == 1))
        self.assertEqual(P((X > 0) & (X < 2)), P(X == 1))
        self.assertEqual(P((X >= 1) & (X <= 1)), P(X == 1))
        self.assertEqual(P((X >= 1) & (X <= 1)), P(X == 1))

    def test_conditional_probability(self):
        self.assertEqual(0.5, P((X == 2) | (X > 1)))
        self.assertEqual(P((X == 2) | (X > 1)), 1 - P((X > 2) | (X > 1)))

