from abc import ABC, abstractmethod
from openlostcat.operators.quantifier_operators import ANY
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator


class AbstractFilterOperator(ABC):
    """Ancestor class for the set-level (filter) operators
    """

    wrapper_quantifier = ANY
    """wrapper_quantifier default
    atomic will default to ANY, IMPL will default to ALL,
    NOT and REF inherits,
    AND will wrap into ALL if each subexprs defaults to ALL otherwise will wrap into ANY
    OR will wrap into ALL if any subexpr defaults to ALL otherwise will wrap into ANY
    """

    def wrap_as_bool_op(self):
        """If a filter operator becomes a top-level operator for a category,
        it must be wrapped into a bool operator by a quantifier - this function is called in this case

        :return:
        """
        return self.wrapper_quantifier(None, self)

    @staticmethod
    def get_as_bool_op(op):
        """

        :param op:
        :return:
        """
        return op.wrap_as_bool_op() if not AbstractBoolOperator.is_bool_op(op) else op

    @staticmethod
    def get_as_bool_op_list(op_list):
        """

        :param op_list:
        :return:
        """
        return [AbstractFilterOperator.get_as_bool_op(op) for op in op_list]
  
    @abstractmethod
    def apply(self, tag_bundle_set):
        """

        :param tag_bundle_set:
        :return:
        """
        return tag_bundle_set
