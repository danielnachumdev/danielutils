import unittest

from danielutils import Stack


class TestStack(unittest.TestCase):
    def test_simple(self):
        s = Stack()
        n = 10
        for i in range(n):
            s.push(i)
        for a, b in zip(range(9, -1, -1), s):
            self.assertEqual(a, b)
