import unittest
from openlostcat.operators.filter_operators import FilterConst
from openlostcat.utils import to_tag_bundle_set


class TestConst(unittest.TestCase):

    def test_simply_const(self):
        """Test the basic functionality
        """
        self.assertFalse(FilterConst(False).apply(to_tag_bundle_set([])))
        self.assertFalse(FilterConst(False).apply(to_tag_bundle_set([{"foo": "void"}])))
        self.assertFalse(FilterConst(False).apply(to_tag_bundle_set([{"foo": "void"}, {"foo2": "void2"}])))
        self.assertFalse(FilterConst(True).apply(to_tag_bundle_set([])))
        self.assertTrue(FilterConst(True).apply(to_tag_bundle_set([{"foo": "void"}])))
        self.assertTrue(FilterConst(True).apply(to_tag_bundle_set([{"foo": "void"}, {"foo2": "void2"}])))


if __name__ == '__main__':
    unittest.main()
