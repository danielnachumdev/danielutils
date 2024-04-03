import unittest

from danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, \
    FunctionDependency as FD  # type:ignore

A, B, C, D, E = AT.create_many(5)


class TestWeek10(unittest.TestCase):
    def test_is_dependency_preservind(self):
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
        self.assertTrue(R.is_decomposition_dependency_preserving([R1, R2, R3], F))

    def test_combined(self):
        """page 2 slide 5
        """
        R = RE([A, B, C, D, E])
        R1 = RE([A, B, D, E])
        R2 = RE([D, E, C])
        F = FDG([
            FD(A, A + B + C + D + E),
            FD(B + C, A),
            FD(D + E, C)
        ])
        self.assertFalse(R.is_BCNF(F))
        self.assertTrue(R.is_3NF(F))
        self.assertTrue(R.is_decomposition_lossless([R1, R2], F))
        self.assertFalse(R.is_decomposition_dependency_preserving([R1, R2], F))

    # def test_compute_projection():
    #     """page 4 slide 4
    #     """
    #     R = RE([A, B, C, D])
    #     R1 = RE([A, C, D])
    #     R1 = RE([B, C])
    #     F = FDG([
    #         FD(A+B, C),
    #         FD(C, A),
    #         FD(C, D)
    #     ])
    #     res = F.project_on(R1)
    #     pass

    def test_minimal_cover(self):
        """page 5 slide 2
        """
        F = FDG([
            FD(A, B),
            FD(B, C),
            FD(A, C),
            FD(A, A),
            FD(C + B, B)
        ])
        self.assertSetEqual(set(F.minimal_cover()), {FD(A, B), FD(B, C)})

    def test_minimal_cover2(self):
        """page 6 slide 5
        """

        G, H, J = AT("G"), AT("H"), AT("J")
        F = FDG([
            FD(A, B),
            FD(A + B + C + D, E),
            FD(E + J, G + H),
            FD(A + C + D + J, E + G),
        ])
        self.assertSetEqual(set(F.minimal_cover()), {FD(A, B), FD(E + J, G), FD(E + J, H), FD(A + C + D, E)})

    def test_find_3NF_1(self):
        """page 9 slide 1
        """
        G, H, J = AT("G"), AT("H"), AT("J")
        R = RE([A, B, C, D, E, G, H, J])
        F = FDG([
            FD(A, B),
            FD(A + B + C + D, E),
            FD(E + J, G + H),
            FD(A + C + D + J, E + G)
        ])
        self.assertSetEqual(set(R.find_3NF_decomposition(F)), {RE([A, B]),
                                                               RE([E, J, G]),
                                                               RE([E, J, H]),
                                                               RE([A, C, D, E]),
                                                               RE([A, J, C, D])})

    def test_find_3NF_2(self):
        """from ex 4
        """
        R = RE.from_string("ABCDEFGHIJKL")
        F = FDG.from_dict({
            "A": "BD",
            "B": "ACD",
            "E": "FGH",
            "F": "GEA",
            "G": "FIJ",
            "EK": "LH",
        })
        got = set(R.find_3NF_decomposition(F))
        expected = {RE.from_string("AB"),
                    RE.from_string("AB"),
                    RE.from_string("BC"),
                    RE.from_string("BD"),
                    RE.from_string("EF"),
                    RE.from_string("EG"),
                    RE.from_string("EH"),
                    RE.from_string("EKL"),
                    RE.from_string("AF"),
                    RE.from_string("FG"),
                    RE.from_string("GI"),
                    RE.from_string("GJ")}
        self.assertSetEqual(got, expected)

    def test_find_BCNF_decomposition(self):
        """page 16 slide 3
        """
        R = RE([A, B, C, D, E])
        F = FDG([
            FD(A + B, C),
            FD(D + E, C),
            FD(B, E)
        ])
        got = set(R.find_BCNF_decomposition(F))
        expected = {
            RE([B, E]),
            RE([A, B, C]),
            RE([A, B, D])
        }
        self.assertSetEqual(got, expected)
