import unittest
from openlostcat.operators.filter_operators import FilterAND, FilterOR, FilterConst, AtomicFilter
from openlostcat.operators.quantifier_operators import ANY, ALL
from tests.filteroperators import test_set
from tests.filteroperators import test_operators_list
from tests.filteroperators import test_tag_bundle_set


class TestAndOr(unittest.TestCase):

    test_operator_list = [AtomicFilter("d", "pass"), AtomicFilter("e", "pass")]

    const_with_any = FilterConst(False)
    const_with_all = FilterConst(False)
    const_with_all.wrapper_quantifier = ALL

    test_wrapper_quantifier_set = [
        [const_with_any, const_with_any, const_with_any, const_with_any],
        [const_with_all, const_with_all, const_with_all, const_with_all],
        [const_with_any, const_with_any, const_with_any, const_with_all],
        [const_with_all, const_with_all, const_with_all, const_with_any]
    ]

    def test_AND(self):
        """Test const case
        """
        validation = [set(), set(), test_tag_bundle_set, set(), set(), set(), test_tag_bundle_set, set()]
        for (test, valid) in list(zip(test_operators_list, validation)):
            with self.subTest(test=test):
                self.assertEqual(FilterAND(test).apply(test_tag_bundle_set), valid)

    def test_OR(self):
        """Test const case
        """
        validation = [test_tag_bundle_set, test_tag_bundle_set, test_tag_bundle_set, set(),
                      test_tag_bundle_set, test_tag_bundle_set, test_tag_bundle_set, set()]
        for (test, valid) in list(zip(test_operators_list, validation)):
            with self.subTest(test=test):
                self.assertEqual(FilterOR(test).apply(test_tag_bundle_set), valid)

    def test_AND_complex(self):
        """Test complex case.
        """
        self.assertEqual(len(FilterAND(self.test_operator_list).apply(test_set)), 1)

    def test_OR_complex(self):
        """Test complex case.
        """
        self.assertEqual(len(FilterOR(self.test_operator_list).apply(test_set)), 3)

    def test_wrapper_quantifier_inheritance_AND(self):
        """Test AND wrapper quantifier return value
        """
        validation = [ANY, ALL, ANY, ANY]
        for (test, valid) in list(zip(self.test_wrapper_quantifier_set, validation)):
            with self.subTest(test=test):
                self.assertEqual(FilterAND(test).wrapper_quantifier, valid)

    def test_wrapper_quantifier_inheritance_OR(self):
        """Test OR wrapper quantifier return value
        """
        validation = [ANY, ALL, ALL, ALL]
        for (test, valid) in list(zip(self.test_wrapper_quantifier_set, validation)):
            with self.subTest(test=test):
                self.assertEqual(FilterOR(test).wrapper_quantifier, valid)


if __name__ == '__main__':
    unittest.main()
