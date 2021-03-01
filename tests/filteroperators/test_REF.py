import unittest
from openlostcat.operators.filter_operators import FilterREF, FilterConst
from openlostcat.operators.quantifier_operators import ANY, ALL
from tests.filteroperators import test_tag_bundle_set


class TestRef(unittest.TestCase):

    def test_simply_ref(self):
        self.assertEqual(FilterREF("#false_ref", FilterConst(False)).apply(test_tag_bundle_set), set())
        self.assertEqual(FilterREF("#true_ref", FilterConst(True)).apply(test_tag_bundle_set), test_tag_bundle_set)

    def test_wrapper_quantifier_inheritance(self):
        """Test wrapper quantifier return value
        """
        const_with_any = FilterConst(False)
        const_with_all = FilterConst(False)
        const_with_all.wrapper_quantifier = ALL
        self.assertEqual(FilterREF("#false_ref", const_with_any).wrapper_quantifier, ANY)
        self.assertEqual(FilterREF("#false_ref", const_with_all).wrapper_quantifier, ALL)


if __name__ == '__main__':
    unittest.main()
