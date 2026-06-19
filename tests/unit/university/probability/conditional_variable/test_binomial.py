import unittest
try:
    from danielutils.university.probability import DiscreteDistribution as D, probability_function as P
    from danielutils import frange
except:
    # python == 3.9.0
    from .....danielutils.university.probability import DiscreteDistribution as D, probability_function as P
    from .....danielutils import frange


class TestBinomial(unittest.TestCase):
    def test_many_ber_is_bin(self):
        for p in frange(0, 1, 0.1):
            for n in range(1, 100):
                Xi = [D.Ber(p) for _ in range(n)]
                X = D.Bin(n, p)
                for k in range(n):
                    self.assertEqual(P(X == k), P(sum(Xi) == k))
