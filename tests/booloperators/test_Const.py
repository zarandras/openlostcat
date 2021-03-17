import unittest
from openlostcat.operators.bool_operators import BoolConst
from openlostcat.utils import to_tag_bundle_set


class TestConst(unittest.TestCase):

    def test_simply_const(self):
        self.assertFalse(BoolConst(False).apply(to_tag_bundle_set([]))[0])
        self.assertFalse(BoolConst(False).apply(to_tag_bundle_set([{"foo": "void"}]))[0])
        self.assertTrue(BoolConst(True).apply(to_tag_bundle_set([]))[0])
        self.assertTrue(BoolConst(True).apply(to_tag_bundle_set([{"foo": "void"}]))[0])


if __name__ == '__main__':
    unittest.main()
