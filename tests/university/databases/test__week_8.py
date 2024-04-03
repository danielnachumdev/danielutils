import unittest

from danielutils import Attribute as AT, FunctionalDependencyGroup as FDG, Relation as RE, \
    FunctionDependency as FD  # type:ignore

A, B, C, D, E = AT.create_many(5)
S, D, H = AT("S"), AT("D"), AT("H")


class TestWeek8(unittest.TestCase):

    def test_follows_from(self):
        # page 10
        F1 = FD(A, B)
        F2 = FD(A, C)
        F3 = FD(C, D)
        F = FDG([F1, F2, F3])
        F4 = FD(A, D)
        self.assertTrue(F4.follows_from(F))
        # page 11
        F5 = FD(D, C)
        self.assertFalse(F5.follows_from(F))

    def test_trivial(self):
        self.assertFalse(FD(A, B).is_trivial())
        self.assertTrue(FD(A + B, A).is_trivial())
        self.assertTrue(FD(A + B, B).is_trivial())
        self.assertTrue(FD(B + A, B).is_trivial())
        self.assertTrue(FD(A + B, B + A).is_trivial())

    def test_closure(self):
        """page 18 slide 3
        """
        F = FDG([FD(A + B, C), FD(A, B), FD(C, D), FD(D, B)])
        self.assertEqual(A.closure(F), AT("ABCD"))
        self.assertEqual(C.closure(F), AT("BCD"))

    def test_superkey(self):
        """page 21 slide 2
        """
        R = RE([S, D, H])
        F = FDG([
            FD(S, D)
        ])
        self.assertTrue(R.is_superkey(S + H, F))

    def test_key(self):
        """page 21 slide 3
        """
        R = RE([S, D, H])
        F = FDG([
            FD(D, H),
            FD(H, D),
        ])
        self.assertTrue(R.is_key(S + D, F))
        self.assertTrue(R.is_key(S + H, F))

    def test_find_key(self):
        """page 21 slide 6
        """
        R = RE([A, B, C, D, E])
        F = FDG([
            FD(A, B),
            FD(B + C, E),
            FD(E + D, A)
        ])
        self.assertEqual(R.find_key(F), C + D + E)
