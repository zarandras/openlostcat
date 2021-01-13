from openlostcat.utils import error
from openlostcat.parsers.utils import  is_bool_op, is_bool_op_list, get_as_bool_op, get_as_bool_op_list, self.__parse_operator
from openlostcat.operators.filter_operators import FilterAND, FilterOR, FilterNOT, AtomicFilter, FilterIMPL
from openlostcat.operators.bool_operators import BoolAND, BoolOR, BoolNOT, BoolConst, BoolIMPL
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.parsers.refdict import RefDict


class OpExpressionParser:
    
    def __init__(self, ref_dict = RefDict()):
        self.ref_dict = ref_dict

    @staticmethod
    def __parse_operator(op, filter_op_class, bool_op_class, check, getLogicalElement = lambda x: x):
        return bool_op_class(getLogicalElement(op)) if check(op) else filter_op_class(op)
        
    def __create__quantifiers(self, name, value, quantifier):
        element = self.__parse_standalone_operator(value)
        if is_bool_op(element):
            error("__" + quantifier.__name__ + " key is not defined for logical operators", v)
        return quantifier(name, element)
    
    def __create_or(self, l):
        return self.__parse_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterOR, BoolOR,
            is_bool_op_list, self.get_as_bool_op_list)

    def __create_and(self, d):
        return self.__parse_operator(
            [self.__parse_keyvalue_operator(t) for t in d.items()],
            FilterAND, BoolAND,
            is_bool_op_list, self.get_as_bool_op_list)
    
    def __create_impl(self, l):
        return self.__parse_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterIMPL, BoolIMPL,
            is_bool_op_list, self.get_as_bool_op_list)

    def __parse_keyvalue_operator(self, t):
        k = t[0]
        v = t[1]
        if k.startswith("__OR"):
            if isinstance(v,list):
                return self.__create_or(v)
            else:
                error("__OR key must contain a list element", v)
        if k.startswith("__AND"):
            if isinstance(v,dict):
                self.__create_and(v)
                return
            else:
                error("__AND key must contain a dict element", v)
        if k.startswith("__NOT"):
            if isinstance(v, list) or isinstance(v, dict):
                return self.__parse_operator(self.__parse_standalone_operator(v), FilterNOT, BoolNOT, is_bool_op)
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
                return self.__create_impl(v)
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
    
    # For JSON items without attribute name (key):
    def __parse_standalone_operator(self, source):
        switcher = {
            list: self.__create_or,
            dict: self.__create_and,
            str: self.ref_dict.get_ref,
            bool: lambda b: BoolConst(b)
        }
        return switcher.get(type(source),
                            lambda x: error("Atomic value is not allowed here: ", x))(source)
    
    def parse_operator(self, source):
        return self.__parse_standalone_operator(source)

    def parse_category(self, rules):
        if isinstance(rules, list):
            # A category-level list is interpreted as a list of bool level rules
            # (each item forced as a bool op instead of a filter-or)
            return BoolOR(self.get_as_bool_op_list([self.__parse_standalone_operator(r) for r in rules]))
        else:
            # Any other json element as category is interpreted as a single bool-level operator
            # (any filter-level ops forced as bool ops by wrapping them into an ANY quantifier)
            return self.get_as_bool_op(self.__parse_standalone_operator(rules))


        # return BoolOR(self.get_as_bool_op_list([self.__parse_standalone_operator(r) for r in rules]))  \
        #     if isinstance(rules,list) \
        #     else self.get_as_bool_op(self.__parse_standalone_operator(rules))

    