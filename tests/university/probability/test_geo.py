import unittest

from danielutils import Geo as G, P


class TestGeo(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(0.25, P(G(0.5) == 1))
