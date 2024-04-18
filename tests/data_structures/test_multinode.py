import unittest
from danielutils.data_structures import MultiNode as N


class TestMultiNode(unittest.TestCase):
    def test_depth(self):
        self.assertEqual(1, N(1).depth())
        self.assertEqual(1, N(1, []).depth())
        self.assertEqual(1, N(1, [None]).depth())
        self.assertEqual(2, N(1, [None, N(1)]).depth())
        self.assertEqual(2, N(1, [N(1), N(1)]).depth())
        self.assertEqual(2, N(1, [N(2), N(3)]).depth())
        self.assertEqual(2, N(1, [N(2,[None]), N(3)]).depth())
        self.assertEqual(3, N(1, [N(2, [N(4)]), N(3)]).depth())
