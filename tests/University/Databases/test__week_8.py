from ....danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, FunctionDependency as FD  # type:ignore


A, B, C, D, E = AT.create_many(5)
S, D, H = AT("S"), AT("D"), AT("H")


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
    """page 18 slide 3
    """
    F = FDG([FD(A+B, C), FD(A, B), FD(C, D), FD(D, B)])
    assert A.closure(F) == AT("ABCD")
    assert C.closure(F) == AT("BCD")


def test_superkey():
    """page 21 slide 2
    """
    R = RE([S, D, H])
    F = FDG([
        FD(S, D)
    ])
    assert R.is_superkey(S+H, F)


def test_key():
    """page 21 slide 3
    """
    R = RE([S, D, H])
    F = FDG([
        FD(D, H),
        FD(H, D),
    ])
    assert R.is_key(S+D, F)
    assert R.is_key(S+H, F)


def test_find_key():
    """page 21 slide 6
    """
    R = RE([A, B, C, D, E])
    F = FDG([
        FD(A, B),
        FD(B+C, E),
        FD(E+D, A)
    ])
    assert R.find_key(F) == C+D+E
