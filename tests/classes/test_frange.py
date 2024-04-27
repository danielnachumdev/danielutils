import unittest

try:
    from danielutils import frange as f
except:
    # python == 3.9.0
    from ...danielutils import frange as f


class TestFrange(unittest.TestCase):
    def test_iteration(self):
        for a, b in zip(range(100), f(100)):
            self.assertEqual(a, b)

        for a, b in zip(range(10, 100), f(10, 100)):
            self.assertEqual(a, b)

        for a, b in zip(range(10, 100, 5), f(10, 100, 5)):
            self.assertEqual(a, b)

    def test_normalization(self):
        for a, b in zip(range(0, 10, 1), f(0, 5, 0.5).normalize()):
            self.assertEqual(a, b)

    def test_contains(self):
        r = f(0, 5, 0.5)
        self.assertIn(1, r)
        self.assertNotIn(1.2, r)
        self.assertIn(0, r)
        self.assertIn(0.5, r)
        self.assertNotIn(5, r)

    def test_find_min_step(self):
        func = f._find_min_step
        self.assertEqual(1, func(1, 0.5))
        self.assertEqual(0.5, func(0.1, 0.5))
        self.assertEqual(3, func(0.6, 0.5))
        self.assertEqual(1, func(0.2, 0.5))

    def test_intersection(self):
        self.assertEqual(f(0, 1, 0.5), f(0, 1, 0.5).intersect(f(0, 1, 0.1)))
        self.assertEqual(f(0), f(1.2, 1.3, 0.95).intersect(f(0, 1, 0.1)))
        self.assertEqual(f(1, 10), f(1, 10, 0.5).intersect(f(1, 10, 0.2)))
        self.assertEqual(f(0, 1, 0.4), f(0, 1, 0.2).intersect(f(0, 1, 0.4)))

    def test__getitem__(self):
        r = f(10)
        self.assertEqual(5, r[5])
        self.assertListEqual(list(range(5)), list(r[:5]))
        self.assertListEqual(list(range(4, -1, -1)), list(r[:5:-1]))
