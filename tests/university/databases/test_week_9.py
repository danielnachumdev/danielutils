from ....danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, FunctionDependency as FD  # type:ignore
A, B, C, D, E = AT.create_many(5)


def test_find_all_keys1():
    """page 1 slide 4
    """
    R = RE([A, B, C, D, E])
    F = FDG([
        FD(B+C, D),
        FD(D, E),
        FD(A, C),
        FD(E, B),
    ])
    assert R.find_all_keys(F) == set([A+B, A+E, A+D])


def test_find_all_keys2():
    """page 1 slide 5
    """
    R = RE([A, B, C, D])
    F = FDG([
        FD(A+B, C),
        FD(C, D+A),
        FD(B+D, C),
        FD(A+D, B),
    ])
    assert R.find_all_keys(F) == set([C, A+B, B+D, A+D])


def test_normal_forms1():
    """page 3 slide 1
    """
    R = RE([A, B, C, D])
    F = FDG([
        FD(A, B+C),
        FD(C, D)
    ])
    assert not R.is_BCNF(F)
    assert not R.is_3NF(F)


def test_normal_forms2():
    """page 3 slide 2
    """
    R = RE([A, B, C, D])
    F = FDG([
        FD(A, B+C),
        FD(C, A+D)
    ])
    assert R.is_BCNF(F)
    assert R.is_3NF(F)


def test_normal_form3():
    """page 3 slide 3
    """
    R = RE([A, B, C])
    F = FDG([])
    assert R.is_BCNF(F)
    assert R.is_3NF(F)


def test_normal_form4():
    """page 4 slide 1
    """
    R = RE([A, B, C])
    F = FDG([FD(A, B), FD(B, A)])
    assert not R.is_BCNF(F)
    assert R.is_3NF(F)

# TODO lossless decomposition @ page 10
