from ....danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, FunctionDependency as FD  # type:ignore
A, B, C, D, E = AT.create_many(5)


def test_is_dependency_preservind():
    R = RE([A, B, C, D])
    R1 = RE([A, B])
    R2 = RE([B, C])
    R3 = RE([C, D])
    F = FDG([
        FD(A, B),
        FD(B, C),
        FD(C, D),
        FD(D, A)
    ])
    assert R.is_preserved_by([R1, R2, R3], F)


def test_combined():
    """page 2 slide 5
    """
    R = RE([A, B, C, D, E])
    R1 = RE([A, B, D, E])
    R2 = RE([D, E, C])
    F = FDG([
        FD(A, A+B+C+D+E),
        FD(B+C, A),
        FD(D+E, C)
    ])
    assert not R.is_BCNF(F)
    assert R.is_3NF(F)
    # TODO is the decomposition loseless
    assert not R.is_preserved_by([R1, R2], F)

# TODO page 4 slide 5


def test_minimal_cover():
    """page 5 slide 2
    """
    F = FDG([
        FD(A, B),
        FD(B, C),
        FD(A, C),
        FD(A, A),
        FD(C+B, B)
    ])
    assert set(F.minimal_cover()) == set([FD(A, C), FD(A, B)])


def test_minimal_cover2():
    """page 6 slide 5
    """

    G, H, J = AT("G"), AT("H"), AT("J")
    F = FDG([
        FD(A, B),
        FD(A+B+C+D, E),
        FD(E+J, G+H),
        FD(A+C+D+J, E+G),
    ])
    assert set(F.minimal_cover()) == set(
        [FD(A, B), FD(E+J, G), FD(E+J, H), FD(A+C+D, E)])


def find_3NF():
    """page 9 slide 1
    """
    G, H, J = AT("G"), AT("H"), AT("J")
    R = RE([A, B, C, D, E, G, H, J])
    F = FDG([
        FD(A, B),
        FD(A+B+C+D, E),
        FD(E+J, G+H),
        FD(A+C+D+J, E+G)
    ])
    assert set(R.find_3NF_decomposition(F)) == set([
        RE([A, B]),
        RE([E, J, G]),
        RE([E, J, H]),
        RE([A, C, D, E]),
        RE([A, J, C, D])
    ])


def test_find_CBNF_decomposition():
    """page 9 slide 1
    """
    R = RE([A, B, C, D, E])
    F = FDG([
        FD(A+B, C),
        FD(D+E, C),
        FD(B, E)
    ])
    assert set(R.find_BCND_decomposition(F)) == set([
        RE([B, E]),
        RE([A, B, C]),
        RE([A, B, D])
    ])
