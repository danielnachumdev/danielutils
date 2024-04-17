import unittest
from danielutils.university.probability import Uniform as U


class TestConditionalVariable(unittest.TestCase):
    def test_equality(self):
        X = U(50)
        self.assertEqual(X > 10, 10 < X)
        self.assertEqual(X >= 10, 10 <= X)
