import functools
from ....danielutils import Attribute  # type:ignore


def test_init():
    Attribute()
    Attribute("")
    Attribute("A")
    Attribute("A")
    Attribute("A")
    Attribute("a")


def test_equallity():
    A = Attribute()
    B = Attribute()
    assert A == B
    C, D = Attribute("A"), Attribute("A")
    assert C == D
    assert A != C
    assert A is not B
    assert A is not A.clone()
    assert A == A.clone()
    assert hash(A) == hash(A.clone())
    assert Attribute("ABCDE") == Attribute("ABCDE"[::-1])
    assert hash(Attribute("ABCDE")) == hash(Attribute("ABCDE"[::-1]))


def test_1():
    ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(1, len(ABC)):
        attributes = Attribute.create_many(i)
        X = functools.reduce(
            lambda prev, curr: prev.union(curr),
            attributes,
        )
        Y = functools.reduce(
            lambda prev, curr: prev+curr,
            attributes,
        )
        assert X == Attribute(ABC[:i]) == Y
        assert Attribute() == X-Y
