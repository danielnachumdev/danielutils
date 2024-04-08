import unittest
from danielutils import ProbabilityFunction as P, ExpectedValue as E, Ber, Unif, Geo, Bin, Pois
from random import randint


def randfloat(a=0, b=1):
    nominator = randint(0, 1_000_000_000)
    denominator = randint(1, 1_000_000_000)
    nominator, denominator = min(nominator, denominator), max(nominator, denominator)
    x = nominator / denominator
    x = x * b + a
    return x


X1, X2, X = Ber(0.5), Ber(0.5), Bin(2, 0.5)


class TestEndToEnd(unittest.TestCase):
    def test_binomial_bernoulli(self):
        self.assertEqual(0, P(X1 + X2 == X))

    def test_expected_value(self):
        for p in (randfloat() for _ in range(1000)):
            self.assertEqual(p, E(Ber(p)))
            self.assertEqual(1 / p, E(Geo(p)))
            for n in range(100):
                self.assertEqual(n * p, E(Bin(n, p)))
            self.assertEqual(p, E(Pois(p)))

    def test_addition(self):
        self.assertEqual(0.25, P(X1 + X2 == 0))
        self.assertEqual(0.5, P(X1 + X2 == 1))
        self.assertEqual(0.25, P(X1 + X2 == 2))
