import unittest

from openlostcat.operators.filter_operators import AtomicFilter, FilterIMPL, FilterConst
from openlostcat.operators.bool_operators import BoolConst
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator
from openlostcat.operators.abstract_filter_operator import AbstractFilterOperator


class TestAbstractFilterOperator(unittest.TestCase):

    def test_wrap_as_bool_op(self):
        """Test Bool operator conversion
        """
        atomic_filter = AtomicFilter("key", "value")
        filter_impl = FilterIMPL([FilterConst(True), FilterConst(False)])
        self.assertFalse(AbstractBoolOperator.is_bool_op(atomic_filter))
        self.assertTrue(AbstractBoolOperator.is_bool_op(atomic_filter.wrap_as_bool_op()))
        self.assertFalse(AbstractBoolOperator.is_bool_op(filter_impl))
        self.assertTrue(AbstractBoolOperator.is_bool_op(filter_impl.wrap_as_bool_op()))

    def test_get_as_bool_op(self):
        """Test Bool operator conversion
        """
        filter_const = FilterConst(True)
        bool_const = BoolConst(True)
        self.assertFalse(AbstractBoolOperator.is_bool_op(filter_const))
        self.assertTrue(AbstractBoolOperator.is_bool_op(AbstractFilterOperator.get_as_bool_op(filter_const)))
        self.assertTrue(AbstractBoolOperator.is_bool_op(bool_const))
        self.assertTrue(AbstractBoolOperator.is_bool_op(AbstractFilterOperator.get_as_bool_op(bool_const)))

    def test_get_as_bool_op_list(self):
        """Test Bool operator list conversion
        """
        filter_op_list = [FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True)]
        bool_op_list = [BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True)]
        mix_op_list = [BoolConst(True), FilterConst(True), BoolConst(True), FilterConst(True)]
        for op_list in [filter_op_list, bool_op_list, mix_op_list]:
            with self.subTest(op_list=op_list):
                self.assertTrue(all(
                    [AbstractBoolOperator.is_bool_op(op) for op in AbstractFilterOperator.get_as_bool_op_list(op_list)]
                ))


if __name__ == '__main__':
    unittest.main()
