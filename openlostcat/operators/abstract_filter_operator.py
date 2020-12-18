from abc import ABC, abstractmethod
from openlostcat.operators.quantifier_operators import ANY

class AbstractFilterOperator(ABC):

    @staticmethod
    def tag_bundle_set_diff(a, b):
#         return [e for e in a if json.dumps(e, sort_keys=True) not in {json.dumps(d, sort_keys=True) for d in b}]
        return list(map(dict, set(frozenset(d.items()) for d in a) - set(frozenset(d.items()) for d in b)))

    def wrap_as_bool_op(self, quantifier = ANY):
        return quantifier(None, self)
  
    @abstractmethod
    def apply(self, tags):
        return tags

 