from abc import ABC, abstractmethod
from openlostcat.operators.quantifier_operators import ANY
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator

class AbstractFilterOperator(ABC):
    """

    """

    wrapper_quantifier = ANY
    """wrapper_quantifier default
    atomic will default to ANY, IMPL will default to ALL,
    NOT and REF inherits,
    AND will wrap into ALL if each subexprs defaults to ALL otherwise will wrap into ANY
    OR will wrap into ALL if any subexpr defaults to ALL otherwise will wrap into ANY
    """

    def wrap_as_bool_op(self):
        """

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
    def get_as_bool_op_list(l, bool_op = ANY):
        """

        :param l:
        :param bool_op:
        :return:
        """
        return [AbstractFilterOperator.get_as_bool_op(op, bool_op) for op in l]
  
    @abstractmethod
    def apply(self, tag_bundle_set ):
        """

        :param tag_bundle_set:
        :return:
        """
        return tags

 