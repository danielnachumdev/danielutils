import unittest
from danielutils import frange
from danielutils.university.probability import Bernoulli as B, probability_function as P, expected_value as E


class TestBernoulli(unittest.TestCase):
    def test_simple(self):
        X = B(0.5)
        self.assertEqual(0.5, P(X == 1))
        self.assertEqual(0.5, P(X == 0))

    def test_expected_value(self):
        for p in frange(0.1, 0.9, 0.01):
            X = B(p)
            self.assertEqual(p, E(X))
            self.assertEqual(P(X == 1), E(X))
            self.assertEqual(1 - P(X == 0), E(X))

    def test_addition_easy(self):
        X = B(0.5)
        self.assertEqual(P(X == 1), P(X + 1 == 2))
        self.assertEqual(P(X == 1), P(1 + X == 2))
        self.assertEqual(P(X == 1), P(1 - X == 0))
        self.assertEqual(P(X == 1), P(X - 1 == 0))

    def test_addition_hard(self):
        for p in frange(0.1, 0.9, 0.01):
            X = B(p)
            self.assertEqual(P(X == 1), P(X + 1 == 2))
            self.assertEqual(P(X == 1), P(1 + X == 2))
            self.assertEqual(P(X == 1), P(1 - X == 0))
            self.assertEqual(P(X == 1), P(X - 1 == 0))

    def test_probability_function(self):
        for p in frange(0.1, 0.9, 0.01):
            X = B(p)
            self.assertEqual(1, P(X <= 1))
            self.assertEqual(1, P(X <= 50))
            self.assertEqual(p, P(X >= 1))
            self.assertEqual(P(X == 1), P(X >= 1))
            self.assertEqual(1, P(X >= 0))
            self.assertEqual(1, P(X > -50))
            self.assertEqual(1, P(X < 70))
