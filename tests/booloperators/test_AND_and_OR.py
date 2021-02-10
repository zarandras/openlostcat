import unittest
from openlostcat.operators.bool_operators import BoolAND, BoolOR, BoolConst
from openlostcat.utils import to_tag_bundle_set


class TestAndOr(unittest.TestCase):
    tests = [
        [BoolConst(False), BoolConst(True)],
        [BoolConst(True), BoolConst(False)],
        [BoolConst(True), BoolConst(True)],
        [BoolConst(False), BoolConst(False)],
        [BoolConst(False), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True)],
        [BoolConst(True), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False)],
        [BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True)],
        [BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False)]
    ]

    def testAnd(self):
        validation = [False, False, True, False, False, False, True, False]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(
                BoolAND(test).apply(to_tag_bundle_set([]))[0], valid)

    def testOR(self):
        validation = [True, True, True, False, True, True, True, False]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(
                BoolOR(test).apply(to_tag_bundle_set([]))[0], valid)



if __name__ == '__main__':
    unittest.main()


