import unittest
from openlostcat.operators.bool_operators import BoolNOT, BoolConst
from openlostcat.utils import to_tag_bundle_set


class TestNot(unittest.TestCase):

    def test_simply_not(self):
        self.assertTrue(BoolNOT(BoolConst(False)).apply(to_tag_bundle_set([]))[0])
        self.assertFalse(BoolNOT(BoolConst(True)).apply(to_tag_bundle_set([]))[0])


if __name__ == '__main__':
    unittest.main()
