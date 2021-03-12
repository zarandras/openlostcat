from abc import ABC, abstractmethod
from openlostcat.operators.quantifier_operators import ANY
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator


class AbstractFilterOperator(ABC):
    """Ancestor class for the set-level (filter) operators
    """

    wrapper_quantifier = ANY
    """ If a set(filter)-level operator(subexpression) becomes a top-level operator(subexpression) for a category, 
    or becomes an operand of a multi-ary operator having bool-level operands,
    the filter-level operator must be wrapped into a bool operator(subexpression) by a quantifier.
    
    wrapper_quantifier is the default wrapper quantifier for a set(filter)-level operator
    wherever a category(bool)-level operator(subexpression) is expected and it must be converted to it:
    
        atomic filters and const filters will default to ANY, implication will default to ALL,
        'not's and references inherit from their subexpression,
        'and' will wrap into ALL if each operand defaults to ALL, otherwise will wrap into ANY by default
        'or' will wrap into ALL if any of the operands defaults to ALL, otherwise will wrap into ANY by default
    """

    def wrap_as_bool_op(self):
        """Wraps the set(filter)-level operator (subexpression) to a category(bool)-level subexpression
        by its appropriate wrapper quantifier

        :return: abstract bool operator (subexpression), actually a quantifier operator
        """
        return self.wrapper_quantifier(None, self)

    @staticmethod
    def get_as_bool_op(op):
        """Gets any operator (subexpression) as a category(bool)-level subexpression
        IF necessary, wrapped by an appropriate quantifier

        :return: abstract bool operator (subexpression)
        """
        return op.wrap_as_bool_op() if not AbstractBoolOperator.is_bool_op(op) else op

    @staticmethod
    def get_as_bool_op_list(op_list):
        """Gets any operator (subexpression) list as a category(bool)-level subexpression list
        IF necessary, wrapped by an appropriate quantifier

        :return: abstract bool operator (subexpression) list
        """
        return [AbstractFilterOperator.get_as_bool_op(op) for op in op_list]
  
    @abstractmethod
    def apply(self, tag_bundle_set):
        """Evaluates the operator (subexpression) for the given tag bundle set

        :param tag_bundle_set: tag bundle set of the osm objects at/near the location
        :return: subset of the input as a result of the operator (subexpression)
        """
        return tag_bundle_set
