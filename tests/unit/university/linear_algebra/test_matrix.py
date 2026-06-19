import unittest
import math
from fractions import Fraction

try:
    from danielutils import Matrix
except:
    # python == 3.9.0
    from ....danielutils import Matrix


class TestMatrix(unittest.TestCase):
    def test_identity(self):
        self.assertListEqual([[1]], Matrix.identity(1)._data)  # type:ignore
        self.assertListEqual([[1, 0], [0, 1]], Matrix.identity(2)._data)  # type:ignore

    def test_add_and_mul(self):
        for size in range(20):
            total = Matrix.identity(size) * 0
            for _ in range(size):
                total += Matrix.identity(size)
            expected = Matrix.identity(size) * size
            self.assertListEqual(expected._data, total._data)  # type:ignore

    def test_sub_and_neg_and_and_mul(self):
        for size in range(20):
            total = Matrix.identity(size) * 0
            for _ in range(size):
                total -= Matrix.identity(size)
            expected = -Matrix.identity(size) * size
            self.assertListEqual(expected._data, total._data)  # type:ignore

    def test_truediv(self):
        k = 3

        def f(i: int, j: int) -> int:
            return i * k + j + 1

        m = Matrix(k, k)
        for i in range(k):
            for j in range(k):
                m[i, j] = f(i, j)
        m /= k
        for i in range(k):
            for j in range(k):
                self.assertEqual(Fraction(f(i, j), k), m[i, j]._data[0][0])

    def test_floordiv(self):
        k = 3

        def f(i: int, j: int) -> int:
            return i * k + j + 1

        m = Matrix(k, k)
        for i in range(k):
            for j in range(k):
                m[i, j] = f(i, j)
        m //= k
        for i in range(k):
            for j in range(k):
                self.assertEqual(math.floor(Fraction(f(i, j), k)), m[i, j]._data[0][0])

    def test_pow(self):
        max_size = 10
        for size in range(2, max_size):
            m = Matrix.random(size, size, seed=123456)
            cur = m
            for k in range(size - 1):
                cur @= m

            self.assertListEqual(cur._data, (m ** size)._data)  # type:ignore
