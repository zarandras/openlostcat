import unittest
from openlostcat.operators.filter_operators import FilterNOT, FilterConst
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.utils import to_tag_bundle_set


class TestNot(unittest.TestCase):

    test_tag_bundle_set = [{"foo": "void"}]

    def test_simply_not(self):
        self.assertEqual(FilterNOT(FilterConst(False)).apply(to_tag_bundle_set(self.test_tag_bundle_set)),
                         self.test_tag_bundle_set)
        self.assertFalse(FilterNOT(FilterConst(True)).apply(to_tag_bundle_set(self.test_tag_bundle_set)), set())

    def test_wrapper_quantifier_inheritance(self):
        const_with_any = FilterConst(False)
        const_with_all = FilterConst(False)
        const_with_all.wrapper_quantifier = ALL
        self.assertEqual(FilterNOT(const_with_any).wrapper_quantifier, ANY)
        self.assertEqual(FilterNOT(const_with_all).wrapper_quantifier, ALL)


if __name__ == '__main__':
    unittest.main()
