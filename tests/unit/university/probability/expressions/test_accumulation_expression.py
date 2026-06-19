import unittest

try:
    from danielutils.university.probability import Geometric as G
except:
    # python == 3.9.0
    from .....danielutils.university.probability import Geometric as G

X = G(0.5)


class TestAccumulationExpression(unittest.TestCase):
    def test_multiple_inequalities(self):
        self.assertEqual((0 < X) < 2, (0 < X) & (X < 2))
        self.assertEqual((0 < X) < 2, (0 < X) < 2)
        self.assertEqual((0 < X) < 2, 0 < (X < 2))

    def test__bool__easy(self):
        self.assertTrue(bool((0 < X) == (0 < X)))
        self.assertTrue(bool((0 < X) == (X > 0)))

    def test__bool__medium(self):
        self.assertTrue((0 < X) == (X > 0))
