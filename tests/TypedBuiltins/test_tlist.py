import random
from typing import Union, Any
import pytest
from ...danielutils.Classes.TypedBuiltins import tlist  # type:ignore
from ...danielutils import isoftype  # type:ignore


def test_basic():
    with pytest.raises(ValueError):
        tlist(1)

    tlist[int]()
    tlist[float]()
    tlist[Union[int, float]]()
    tlist[Union[int, float]]()
    tlist[Any]()


def test_correct_values():
    tlist[int]([1, 2, 3, 4])
    tlist[float]([0.1, 0.1, 0.2])
    tlist[Union[int, float]]([1, 2, 3, 0.1, 0.2])
    tlist[Union[int, float]]([1, 23, 3, 0.1, 0.2])
    tlist[Any]([1, 2, 0.2, 0.63, [], [1]])


def test_wrong_values():
    with pytest.raises(TypeError):
        tlist[float]([1, 2, 3, 4])
    with pytest.raises(TypeError):
        tlist[int]([1, 2, 3, "4"])
    with pytest.raises(TypeError):
        tlist[Union[int, float]]([1, 2.2, 3, "4"])
    with pytest.raises(TypeError):
        tlist[tuple[int]]([[1], [2], [3], ["4"]])


def test_isinstance():
    assert isinstance([1, 2, 3, 4], tlist[int])
    assert isinstance([0.1, 0.1, 0.2], tlist[float])
    assert isinstance([1, 2, 3, 0.1, 0.2], tlist[Union[int, float]])
    assert isinstance([1, 23, 3, 0.1, 0.2], tlist[Union[int, float]])
    assert isinstance([1, 2, 0.2, 0.63, [], [1]], tlist[Any])


def test_isinstanse_fail():
    assert not isinstance([1, 2, 3, "4"], tlist[int])
    assert not isinstance([0.1, 0.1, " 0.2"], tlist[float])
    assert not isinstance([1, 2, 3, 0.1, "0.2"], tlist[Union[int, float]])
    assert not isinstance([1, 23, 3, 0.1, " 0.2"], tlist[Union[int, float]])


def test_isinstance_with_regular_list():
    a = tlist[int]([1, 2, 3])
    assert isinstance(a, list)
    assert isoftype(a, list[int])
    assert isoftype(a, list[Union[int, float]])


def test_extend():
    for _ in range(100):
        l = []
        for __ in range(10):
            l.append(random.randint(0, 100))

        a = tlist[int](l)

        # test copy constructor
        b = tlist[int](a)

        a.extend(b)

        # check addition, multiplication and equality
        assert a == b+b == b*2, "all tlists should be equal"
