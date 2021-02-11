import unittest
from openlostcat.operators.bool_operators import BoolAND, BoolOR, BoolConst, BoolNOT
from openlostcat.utils import to_tag_bundle_set


class TestDeMorgan(unittest.TestCase):
    test_operators_list = [
        [BoolConst(False), BoolConst(True)],
        [BoolConst(True), BoolConst(False)],
        [BoolConst(True), BoolConst(True)],
        [BoolConst(False), BoolConst(False)]
    ]

    @staticmethod
    def get_de_morgan_A1(bool_const_operators):
        return BoolNOT(BoolOR(bool_const_operators))

    @staticmethod
    def get_de_morgan_A2(bool_const_operators):
        return BoolAND([BoolNOT(op) for op in bool_const_operators])

    @staticmethod
    def get_de_morgan_B1(bool_const_operators):
        return BoolNOT(BoolAND(bool_const_operators))

    @staticmethod
    def get_de_morgan_B2(bool_const_operators):
        return BoolOR([BoolNOT(op) for op in bool_const_operators])

    def test_de_morgan(self):
        for test_operators in self.test_operators_list:
            self.assertEqual(TestDeMorgan.get_de_morgan_A1(test_operators).apply(to_tag_bundle_set([]))[0],
                             TestDeMorgan.get_de_morgan_A2(test_operators).apply(to_tag_bundle_set([]))[0])
            self.assertEqual(TestDeMorgan.get_de_morgan_B1(test_operators).apply(to_tag_bundle_set([]))[0],
                             TestDeMorgan.get_de_morgan_B2(test_operators).apply(to_tag_bundle_set([]))[0])


if __name__ == '__main__':
    unittest.main()
