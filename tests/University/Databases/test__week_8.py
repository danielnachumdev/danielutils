from ....danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, FunctionDependency as FD  # type:ignore


A, B, C, D = AT.create_many(4)


def test_follows_from():
    # page 10
    F1 = FD(A, B)
    F2 = FD(A, C)
    F3 = FD(C, D)
    F = FDG([F1, F2, F3])
    F4 = FD(A, D)
    assert F4.follows_from(F)
    # page 11
    F5 = FD(D, C)
    assert not F5.follows_from(F)


def test_trivial():
    assert not FD(A, B).is_trivial()
    assert FD(A+B, A).is_trivial()
    assert FD(A+B, B).is_trivial()
    assert FD(B+A, B).is_trivial()
    assert FD(A+B, B+A).is_trivial()


def test_closure():
    F = FDG([FD(A+B, C), FD(A, B), FD(C, D), FD(D, B)])
    assert A.closure(F) == AT("ABCD")
    assert C.closure(F) == AT("BCD")
