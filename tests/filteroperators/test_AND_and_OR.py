import unittest
from openlostcat.operators.filter_operators import FilterAND, FilterOR, FilterConst
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

    test_tag_bundle_set = [{"foo": "void"}]

    def test_AND(self):
        validation = [set(), set(), self.test_tag_bundle_set, set(), set(), set(), self.test_tag_bundle_set, set()]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(
                FilterAND(test).apply(to_tag_bundle_set(self.test_tag_bundle_set)), valid)

    def test_OR(self):
        validation = [self.test_tag_bundle_set, self.test_tag_bundle_set, self.test_tag_bundle_set, set(),
                      self.test_tag_bundle_set, self.test_tag_bundle_set, self.test_tag_bundle_set, set()]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(
                FilterOR(test).apply(to_tag_bundle_set(self.test_tag_bundle_set)), valid)


if __name__ == '__main__':
    unittest.main()
