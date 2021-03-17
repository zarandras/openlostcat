import unittest
from openlostcat.operators.bool_operators import BoolREF, BoolConst
from openlostcat.utils import to_tag_bundle_set


class TestRef(unittest.TestCase):

    def test_simply_not(self):
        self.assertTrue(BoolREF("##true_ref", BoolConst(True)).apply(to_tag_bundle_set([]))[0])
        self.assertFalse(BoolREF("##false_ref", BoolConst(False)).apply(to_tag_bundle_set([]))[0])


if __name__ == '__main__':
    unittest.main()
