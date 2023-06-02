import time
from ...danielutils.Generators.join_generators import *


def test_simple_case():
    # if this value is too low the result is not deterministic
    MAX_DURATION = 0.5

    def gen1():
        N = 10
        for i in range(N):
            time.sleep((i/N)*MAX_DURATION)
            yield i

    def gen2():
        N = 10
        for i in range(N):
            time.sleep(MAX_DURATION - (i/N)*MAX_DURATION)
            yield i
    res = []
    for v in join_generators_busy_waiting(gen1(), gen2()):
        res.append(v)

    assert res == [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (0, 4), (0, 5), (1, 1), (0, 6),
                   (1, 2), (0, 7), (1, 3), (0, 8), (1, 4), (1, 5), (0, 9), (1, 6), (1, 7), (1, 8), (1, 9)]


def test_simple_case2():
    MAX_DURATION = 0.5

    def gen1():
        N = 10
        for i in range(N):
            time.sleep((i/N)*MAX_DURATION)
            yield i

    def gen2():
        N = 10
        for i in range(N):
            time.sleep(MAX_DURATION - (i/N)*MAX_DURATION)
            yield i
    res = []
    for v in join_generators(gen1(), gen2()):
        res.append(v)
    assert res == [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (0, 4), (0, 5), (1, 1), (0, 6),
                   (1, 2), (0, 7), (1, 3), (0, 8), (1, 4), (1, 5), (0, 9), (1, 6), (1, 7), (1, 8), (1, 9)]
