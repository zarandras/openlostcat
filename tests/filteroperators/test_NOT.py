import unittest
from openlostcat.operators.filter_operators import FilterNOT, FilterConst, AtomicFilter
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.utils import to_tag_bundle_set


class TestNot(unittest.TestCase):

    test_tag_bundle_set = to_tag_bundle_set([{"foo": "void"}])

    test_set = to_tag_bundle_set([
        {
            "a": "yes",
            "c": "fail",
            "d": "pass",
            "e": "fail"
        },
        {
            "a": "no",
            "b": "2",
            "d": "fail",
            "e": "pass"
        },
        {
            "c": "pass",
            "d": "pass",
            "e": "pass"
        },
        {
            "c": "fail"
        }
    ])

    def test_simply_not(self):
        """Test const case
        """
        self.assertEqual(FilterNOT(FilterConst(False)).apply(self.test_tag_bundle_set), self.test_tag_bundle_set)
        self.assertFalse(FilterNOT(FilterConst(True)).apply(self.test_tag_bundle_set), set())

    def test_complex_not(self):
        """Test complex case
        """
        self.assertEqual(FilterNOT(AtomicFilter("a", [None, True])).apply(self.test_set), 1)

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
