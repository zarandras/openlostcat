from openlostcat.utils import error
from openlostcat.parsers.utils import  is_bool_op, is_bool_op_list, get_as_bool_op, get_as_bool_op_list, choose_operator
from openlostcat.operators.filter_operators import FilterAND, FilterOR, FilterNOT, AtomicFilter, FilterIMPL
from openlostcat.operators.bool_operators import BoolAND, BoolOR, BoolNOT, BoolConst, BoolIMPL
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.parsers.refdict import RefDict


class OpExpressionParser:

    get_ANY_wrapped_list = lambda self, x: get_as_bool_op_list(x, ANY)
    get_ANY_wrapped = lambda self, x: get_as_bool_op(x, ANY)
    
    def __init__(self, ref_dict = RefDict()):
        self.ref_dict = ref_dict
        
    def __create__quantifiers(self, name, value, quantifier):
        element = self.__parse_standalone_operator(value)
        if is_bool_op(element):
            error("__" + quantifier.__name__ + " key is not defined for logical operators", v)
        return quantifier(name, element)
    
    def __get_or(self, l):
        return choose_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterOR, BoolOR,
            is_bool_op_list, self.get_ANY_wrapped_list)

    def __get_and(self, d):
        return choose_operator(
            [self.__parse_keyvalue_operator(t) for t in d.items()],
            FilterAND, BoolAND,
            is_bool_op_list, self.get_ANY_wrapped_list)
    
    def __get_impl(self, l):
        return choose_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterIMPL, BoolIMPL,
            is_bool_op_list, self.get_ANY_wrapped_list)

    def __parse_keyvalue_operator(self, t):
        k = t[0]
        v = t[1]
        if k.startswith("__OR"):
            if isinstance(v,list):
                return self.__get_or(v)
            else:
                error("__OR key must contain a list element", v)
        if k.startswith("__AND"):
            if isinstance(v,dict):
                self.__get_and(v)
                return
            else:
                error("__AND key must contain a dict element", v)
        if k.startswith("__NOT"):
            if isinstance(v, list) or isinstance(v, dict):
                return choose_operator(self.__parse_standalone_operator(v), FilterNOT, BoolNOT, is_bool_op)
            else:
                error("__NOT must contain a list or dict elements", v)
        if k.startswith("__REF"):
            if isinstance(v, str):
               # return self.__get_ref(v)
               return self.ref_dict.get_ref(v)
            else:
               error("__REF must contain a string elements", v)   
        if k.startswith("__IMPL"):
            if isinstance(v,list):
                return self.__get_impl(v)
            else:
                error("__IMPL key must contain a list element", v)
        if k.startswith("__BOOLCONST"):
            return BoolConst(v)
        if k.startswith("__ANY"):
            return self.__create__quantifiers(k, v, ANY)
        if k.startswith("__ALL"):
            return self.__create__quantifiers(k, v, ALL)
        if isinstance(v, dict):
            error("AtomicFilter rule must contain a list or single value elements", v)
        return AtomicFilter(k, v)
    
    
    def __parse_standalone_operator(self, source):
        switcher = {
            list: self.__get_or,
            dict: self.__get_and,
            str: self.ref_dict.get_ref,
            bool: lambda b: BoolConst(b)
        }
        return switcher.get(type(source),
                            lambda x: error("Atomic value is not allowed here: ", x))(source)
    
    def parse_operator(self, source):
        return self.__parse_standalone_operator(source)

    def parse_category(self, rules):
        return BoolOR(self.get_ANY_wrapped_list([self.__parse_standalone_operator(r) for r in rules]))  \
            if isinstance(rules,list) \
            else self.get_ANY_wrapped(self.__parse_standalone_operator(rules))

    