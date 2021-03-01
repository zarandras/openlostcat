import unittest
from openlostcat.operators.filter_operators import FilterNOT, FilterConst, AtomicFilter
from openlostcat.operators.quantifier_operators import ANY, ALL
from tests.filteroperators import test_set
from tests.filteroperators import test_tag_bundle_set


class TestNot(unittest.TestCase):

    def test_simply_not(self):
        """Test const case
        """
        self.assertEqual(FilterNOT(FilterConst(False)).apply(test_tag_bundle_set), test_tag_bundle_set)
        self.assertFalse(FilterNOT(FilterConst(True)).apply(test_tag_bundle_set), set())

    def test_complex_not(self):
        """Test complex case
        """
        self.assertEqual(len(FilterNOT(AtomicFilter("a", [None, True])).apply(test_set)), 1)

    def test_wrapper_quantifier_inheritance(self):
        """Test wrapper quantifier return value
        """
        const_with_any = FilterConst(False)
        const_with_all = FilterConst(False)
        const_with_all.wrapper_quantifier = ALL
        self.assertEqual(FilterNOT(const_with_any).wrapper_quantifier, ANY)
        self.assertEqual(FilterNOT(const_with_all).wrapper_quantifier, ALL)


if __name__ == '__main__':
    unittest.main()
