import unittest
from danielutils import Bernoulli as B, ProbabilityFunction as P, frange, ExpectedValue as E


class TestBernoulli(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(0.5, P(B(0.5) == 1))
        self.assertEqual(0.5, P(B(0.5) == 0))

    def test_expected_value(self):
        for p in frange(0.1, 0.9, 0.01):
            self.assertEqual(p, E(B(p)))
