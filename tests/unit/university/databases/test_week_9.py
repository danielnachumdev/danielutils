import unittest

try:
    from danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, \
        FunctionDependency as FD  # type:ignore
except:
    # python == 3.9.0
    from ....danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, \
        FunctionDependency as FD  # type:ignore

A, B, C, D, E = AT.create_many(5)


class TestWeek9(unittest.TestCase):

    def test_find_all_keys1(self):
        """page 1 slide 4
        """
        R = RE([A, B, C, D, E])
        F = FDG([
            FD(B + C, D),
            FD(D, E),
            FD(A, C),
            FD(E, B),
        ])
        self.assertSetEqual(R.find_all_keys(F), {A + B, A + E, A + D})

    def test_find_all_keys2(self):
        """page 1 slide 5
        """
        R = RE([A, B, C, D])
        F = FDG([
            FD(A + B, C),
            FD(C, D + A),
            FD(B + D, C),
            FD(A + D, B),
        ])
        self.assertSetEqual(R.find_all_keys(F), {C, A + B, B + D, A + D})

    def test_normal_forms1(self):
        """page 3 slide 1
        """
        R = RE([A, B, C, D])
        F = FDG([
            FD(A, B + C),
            FD(C, D)
        ])
        self.assertFalse(R.is_BCNF(F))
        self.assertFalse(R.is_3NF(F))

    def test_normal_forms2(self):
        """page 3 slide 2
        """
        R = RE([A, B, C, D])
        F = FDG([
            FD(A, B + C),
            FD(C, A + D)
        ])
        self.assertTrue(R.is_BCNF(F))
        self.assertTrue(R.is_3NF(F))

    def test_normal_form3(self):
        """page 3 slide 3
        """
        R = RE([A, B, C])
        F = FDG([])
        self.assertTrue(R.is_BCNF(F))
        self.assertTrue(R.is_3NF(F))

    def test_normal_form4(self):
        """page 4 slide 1
        """
        R = RE([A, B, C])
        F = FDG([FD(A, B), FD(B, A)])
        self.assertFalse(R.is_BCNF(F))
        self.assertTrue(R.is_3NF(F))

    # TODO lossless decomposition @ page 10
