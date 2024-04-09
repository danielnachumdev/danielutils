import unittest
from danielutils import total_ordering


class TestTotalOrdering(unittest.TestCase):
    def test_simple(self):
        @total_ordering
        class A:
            def __init__(self, v) -> None:
                self.v = v

            def __eq__(self, other):
                return self.v == other.v

            def __gt__(self, other):
                return self.v > other.v

        self.assertEqual(A(1), A(1))
        self.assertNotEqual(A(1), A(2))
        self.assertLess(A(1), A(2))
        self.assertLessEqual(A(1), A(1))
        self.assertLessEqual(A(1), A(2))
        self.assertGreater(A(2), A(1))
        self.assertGreaterEqual(A(2), A(2))
