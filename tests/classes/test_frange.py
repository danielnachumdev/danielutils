import unittest
from danielutils import frange


class TestFrange(unittest.TestCase):
    def test_iteration(self):
        for a, b in zip(range(100), frange(100)):
            self.assertEqual(a, b)

        for a, b in zip(range(10, 100), frange(10, 100)):
            self.assertEqual(a, b)

        for a, b in zip(range(10, 100, 5), frange(10, 100, 5)):
            self.assertEqual(a, b)

    def test_normalization(self):
        for a, b in zip(range(0, 10, 1), frange(0, 5, 0.5).normalize()):
            self.assertEqual(a, b)

    def test_contains(self):
        r = frange(0, 5, 0.5)
        self.assertIn(1, r)
        self.assertNotIn(1.2, r)
        self.assertIn(0, r)
        self.assertIn(0.5, r)
        self.assertNotIn(5, r)

    def test_intersection(self):
        self.assertEqual(frange(0, 2), frange(0, 1, 0.5).intersect(frange(0, 1, 0.1)))
        self.assertEqual(frange(0, 0), frange(1.2, 1.3, 0.95).intersect(frange(0, 1, 0.1)))
