from openlostcat.operators.bool_operators import BoolREF
from openlostcat.operators.quantifier_operators import ANY
from openlostcat.operators.filter_operators import FilterREF
from openlostcat.utils import error
from openlostcat.parsers.utils import is_bool_op


class RefDict:

    def __init__(self, filter_ref_dict = {}, bool_ref_dict = {}):
        self.bool_ref_dict = bool_ref_dict
        self.filter_ref_dict = filter_ref_dict

    @staticmethod
    def is_ref(ref):
        return ref[0].startswith("#")

    @staticmethod
    def is_bool_ref(ref):
        return ref[0].startswith("##")

    def get_ref(self, ref):
        return self.__ref_search(ref)

    @staticmethod
    def __lookfor_ref(r, dic, error_func):
        try:
            ref = dic[r]
        except KeyError:
            ref = error_func(r)
        return ref

    def __ref_search(self, r):
        error_func = lambda x: error("The given reference can not be found: ", x)
        if r.startswith("##"):
            return self.__lookfor_ref(r, self.bool_ref_dict, error_func)
        elif r.startswith("#"):
            return self.__lookfor_ref(r, self.filter_ref_dict, error_func)
        else:
            return self.__lookfor_ref("#" + r, self.filter_ref_dict,
                                      lambda x: self.__lookfor_ref("##" + r, self.bool_ref_dict, error_func))

    def set_ref(self, ref, parser):
        if not self.is_ref(ref):
            error("Invalid reference definition. A reference name must start with '#': ", ref[0])
        op = parser.parse_operator(ref[1])
        if self.is_bool_ref(ref):
            self.bool_ref_dict[ref[0]] = BoolREF(ref[0], op.wrap_as_bool_op(ANY) if not is_bool_op(op) else op)
        else:
            if is_bool_op(op):
                error("Invalid reference definition. A bool expression is given but a filter expression is expected: ", op)
            self.filter_ref_dict[ref[0]] = FilterREF(ref[0], op)

