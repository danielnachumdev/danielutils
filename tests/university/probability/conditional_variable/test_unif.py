import unittest
from danielutils import Unif, ProbabilityFunction as P

N = 100
X = Unif(N)


class TestUnif(unittest.TestCase):
    def test_unif_supp(self):
        self.assertNotIn(0, X.supp)
        self.assertIn(N, X.supp)

    def test_unif(self):
        for i in range(1, N + 1):
            self.assertEqual(1 / N, P(X == i))
