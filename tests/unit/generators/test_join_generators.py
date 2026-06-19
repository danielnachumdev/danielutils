import unittest
from typing import Generator
import time
try:
    from danielutils.generators.join_generators import join_generators, join_generators_busy_waiting  # type:ignore
except:
    # python == 3.9.0
    from ...danielutils.generators.join_generators import join_generators, join_generators_busy_waiting  # type:ignore

EXPECTED = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (0, 4), (0, 5), (1, 1), (0, 6),
            (1, 2), (0, 7), (1, 3), (0, 8), (1, 4), (1, 5), (0, 9), (1, 6), (1, 7), (1, 8),
            (1, 9)]


class TestJoinGenerators(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import random
        random.seed(17)

    def test_simple_case(self):
        # if this value is too low the result is not deterministic
        MAX_DURATION = 0.5

        def gen1() -> Generator:
            N = 10
            for i in range(N):
                time.sleep((i / N) * MAX_DURATION)
                yield i

        def gen2() -> Generator:
            N = 10
            for i in range(N):
                time.sleep(MAX_DURATION - (i / N) * MAX_DURATION)
                yield i

        res = []
        for v in join_generators_busy_waiting(gen1(), gen2()):
            res.append(v)

        self.assertListEqual(EXPECTED, res)

    def test_simple_case2(self):
        MAX_DURATION = 0.5

        def gen1() -> Generator:
            N = 10
            for i in range(N):
                time.sleep((i / N) * MAX_DURATION)
                yield i

        def gen2() -> Generator:
            N = 10
            for i in range(N):
                time.sleep(MAX_DURATION - (i / N) * MAX_DURATION)
                yield i

        res = []
        for v in join_generators(gen1(), gen2()):
            res.append(v)

        self.assertListEqual(EXPECTED, res)
