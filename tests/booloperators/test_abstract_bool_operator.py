import unittest

from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator
from openlostcat.operators.filter_operators import FilterConst
from openlostcat.operators.bool_operators import BoolConst


class TestAbstractBoolOperator(unittest.TestCase):

    def test_get_name(self):
        """Test get_name
        """
        default_name = "name"
        self.assertEqual(default_name, AbstractBoolOperator.get_name("", default_name, []))
        self.assertTrue(AbstractBoolOperator.get_name("", None, "some hashable type"))
        self.assertTrue(AbstractBoolOperator.get_name("", "", "some hashable type"))

    def test_is_bool_op(self):
        """Test is_bool_op functionality - whether an operator is a filter-level or a bool-level (quantified) one
        """
        filter_const = FilterConst(True)
        bool_const = BoolConst(True)
        self.assertFalse(AbstractBoolOperator.is_bool_op(filter_const))
        self.assertTrue(AbstractBoolOperator.is_bool_op(bool_const))

    def test_is_bool_op_list(self):
        """Test is_bool_op_list functionality - if a bool-level operator appears in a list, it becomes a bool-level list
        """
        filter_op_list = [FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True)]
        bool_op_list = [BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True)]
        mix_op_list = [BoolConst(True), FilterConst(True), BoolConst(True), FilterConst(True)]
        validate = [False, True, True]
        for op_list_validation in zip(validate, [filter_op_list, bool_op_list, mix_op_list]):
            with self.subTest(op_list_validation=op_list_validation):
                self.assertEqual(op_list_validation[0], AbstractBoolOperator.is_bool_op_list(op_list_validation[1]))


if __name__ == '__main__':
    unittest.main()
