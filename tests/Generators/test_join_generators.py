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

    assert res == [0, 1, 2, 3, 0, 4, 5, 1, 6, 2, 7, 3, 8, 4, 5, 9, 6, 7, 8, 9]


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

    assert res == [0, 1, 2, 3, 0, 4, 5, 1, 6, 2, 7, 3, 8, 4, 5, 9, 6, 7, 8, 9]
