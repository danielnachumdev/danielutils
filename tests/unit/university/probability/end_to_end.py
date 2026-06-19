import unittest
from danielutils.university.probability import probability_function as P, expected_value as E, DiscreteDistribution as D
from random import uniform

X1, X2, X = D.Ber(0.5), D.Ber(0.5), D.Bin(2, 0.5)


class TestEndToEnd(unittest.TestCase):
    def test_binomial_bernoulli(self):
        self.assertEqual(0, P(X1 + X2 == X))

    def test_expected_value(self):
        for p in (uniform(0, 1) for _ in range(1000)):
            self.assertEqual(p, E(D.Ber(p)))
            self.assertEqual(1 / p, E(D.Geo(p)))
            for n in range(100):
                self.assertEqual(n * p, E(D.Bin(n, p)))
            self.assertEqual(p, E(D.Pois(p)))

    def test_addition(self):
        self.assertEqual(0.25, P(X1 + X2 == 0))
        self.assertEqual(0.5, P(X1 + X2 == 1))
        self.assertEqual(0.25, P(X1 + X2 == 2))
