import unittest
from danielutils.university.probability import Uniform as U


class TestConditionalVariable(unittest.TestCase):
    def test_equality(self):
        X = U(50)
        self.assertTrue((X > 10).is_equal(10 < X))
        self.assertTrue((X >= 10).is_equal(10 <= X))
