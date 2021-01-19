from abc import ABC, abstractmethod
from openlostcat.operators.quantifier_operators import ANY
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator

class AbstractFilterOperator(ABC):

    @staticmethod
    def tag_bundle_set_diff(a, b):
#         return [e for e in a if json.dumps(e, sort_keys=True) not in {json.dumps(d, sort_keys=True) for d in b}]
        return list(map(dict, set(frozenset(d.items()) for d in a) - set(frozenset(d.items()) for d in b)))

    wrapper_quantifier = ANY
    # move it to each filter operator: atomic will default to ANY, IMPL will default to ALL,
    #   NOT and REF inherits,
    #   AND will wrap into ALL if each subexprs defaults to ALL otherwise will wrap into ANY
    #   OR will wrap into ALL if any subexpr defaults to ALL otherwise will wrap into ANY

    def wrap_as_bool_op(self):
        return self.wrapper_quantifier(None, self)

    @staticmethod
    def get_as_bool_op(op, wrapper_bool_op = ANY):
        return op.wrap_as_bool_op() if not AbstractBoolOperator.is_bool_op(op) else op

    @staticmethod
    def get_as_bool_op_list(l, bool_op = ANY):
        return [AbstractFilterOperator.get_as_bool_op(op, bool_op) for op in l]
  
    @abstractmethod
    def apply(self, tags):
        return tags

 