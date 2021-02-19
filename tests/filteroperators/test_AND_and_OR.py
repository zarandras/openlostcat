import unittest
from openlostcat.operators.filter_operators import FilterAND, FilterOR, FilterConst, AtomicFilter
from openlostcat.utils import to_tag_bundle_set


class TestAndOr(unittest.TestCase):
    tests = [
        [FilterConst(False), FilterConst(True)],
        [FilterConst(True), FilterConst(False)],
        [FilterConst(True), FilterConst(True)],
        [FilterConst(False), FilterConst(False)],
        [FilterConst(False), FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True)],
        [FilterConst(True), FilterConst(False), FilterConst(False), FilterConst(False), FilterConst(False)],
        [FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True)],
        [FilterConst(False), FilterConst(False), FilterConst(False), FilterConst(False), FilterConst(False)]
    ]

    test_operator_list = [AtomicFilter("d", "pass"), AtomicFilter("e", "pass")]

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

    test_tag_bundle_set = to_tag_bundle_set([{"foo": "void"}])

    def test_AND(self):
        """Test const case
        """
        validation = [set(), set(), self.test_tag_bundle_set, set(), set(), set(), self.test_tag_bundle_set, set()]
        for (test, valid) in list(zip(self.tests, validation)):
            with self.subTest(test=test):
                self.assertEqual(FilterAND(test).apply(self.test_tag_bundle_set), valid)

    def test_OR(self):
        """Test const case
        """
        validation = [self.test_tag_bundle_set, self.test_tag_bundle_set, self.test_tag_bundle_set, set(),
                      self.test_tag_bundle_set, self.test_tag_bundle_set, self.test_tag_bundle_set, set()]
        for (test, valid) in list(zip(self.tests, validation)):
            with self.subTest(test=test):
                self.assertEqual(FilterOR(test).apply(self.test_tag_bundle_set), valid)

    def test_AND_complex(self):
        """Test complex case.
        """
        self.assertEqual(len(FilterAND(self.test_operator_list).apply(self.test_tag_bundle_set)), 1)

    def test_OR_complex(self):
        """Test complex case.
        """
        self.assertEqual(len(FilterOR(self.test_operator_list).apply(self.test_tag_bundle_set)), 3)


if __name__ == '__main__':
    unittest.main()
