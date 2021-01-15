from openlostcat.utils import error
from openlostcat.parsers.utils import  is_bool_op, is_bool_op_list, get_as_bool_op, get_as_bool_op_list
from openlostcat.operators.filter_operators import FilterAND, FilterOR, FilterNOT, AtomicFilter, FilterIMPL
from openlostcat.operators.bool_operators import BoolAND, BoolOR, BoolNOT, BoolConst, BoolIMPL
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.parsers.refdict import RefDict
import re


class OpExpressionParser:
    
    def __init__(self, ref_dict = RefDict()):
        self.ref_dict = ref_dict

    @staticmethod
    def __parse_list_operator(op, filter_op_class, bool_op_class):
        return bool_op_class(get_as_bool_op_list(op)) if is_bool_op_list(op) else filter_op_class(op)
    
    def __create_or(self, l):
        return self.__parse_list_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterOR, BoolOR)

    def __create_and(self, d):
        return self.__parse_list_operator(
            [self.__parse_keyvalue_operator(*t) for t in d.items()],
            FilterAND, BoolAND)
    
    def __create_impl(self, l):
        return self.__parse_list_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterIMPL, BoolIMPL)

    def __create_not(self, source):
        choose_operator = lambda op, filter_op_class, bool_op_class: bool_op_class(op) if is_bool_op(op) else filter_op_class(op)
        return choose_operator(self.__parse_standalone_operator(source),
                FilterNOT, BoolNOT)

    @staticmethod
    def __get_operator_prefix(key_str):
        try:
            return re.findall("^__([^_]*)_", key_str)[0]
        except IndexError:
            return ""

    @staticmethod
    def __check_json_type(source, type_list):
        return any(isinstance(source, type_candidate) for type_candidate in type_list)
        # for type_candidate in type_list:
        #     if isinstance(source, type_candidate):
        #         return True
        # return False

    def __parse_keyvalue_operator(self, k, v):
        create_and_check =lambda x, create_fv, type_list, error_message : create_fv(x) \
            if self.__check_json_type(x, type_list) \
            else error(error_message, x)
        switcher = {
            "OR": lambda x:  create_and_check(x, self.__create_or, [list], "__OR_ key must contain a list element"),
            "AND": lambda x:  create_and_check(x, self.__create_and, [dict], "__AND_ key must contain a dict element"),
            "NOT": lambda x:  create_and_check(x, self.__create_not, [list, dict], "__NOT_ must contain a list or dict elements"),
            "REF": lambda x:  create_and_check(x, self.ref_dict.get_ref, [str], "__REF_ must contain a string elements"),
            "IMPL": lambda x:  create_and_check(x, self.__create_impl, [list], "__IMPL_ key must contain a list element"),
            "BOOLCONST": lambda x:  create_and_check(x, BoolConst, [bool], "__BOOLCONST_ key must contain a bool element"),
            "ANY": lambda x:  ANY(k, self.__parse_standalone_operator(x)),
            "ALL": lambda x:  ALL(k, self.__parse_standalone_operator(x))
        }
        return switcher.get(self.__get_operator_prefix(k), lambda x:  AtomicFilter(k, x))(v)

    # For JSON items without attribute name (key):
    def __parse_standalone_operator(self, source):
        switcher = {
            list: self.__create_or,
            dict: self.__create_and,
            str: self.ref_dict.get_ref,
            bool: BoolConst
        }
        return switcher.get(type(source),
                            lambda x: error("Atomic value is not allowed here: ", x))(source)
    
    def parse_operator(self, source):
        return self.__parse_standalone_operator(source)

    def parse_category(self, rules):
        if isinstance(rules, list):
            # A category-level list is interpreted as a list of bool level rules
            # (each item forced as a bool op instead of a filter-or)
            return BoolOR(get_as_bool_op_list([self.__parse_standalone_operator(r) for r in rules]))
        else:
            # Any other json element as category is interpreted as a single bool-level operator
            # (any filter-level ops forced as bool ops by wrapping them into an ANY quantifier)
            return get_as_bool_op(self.__parse_standalone_operator(rules))

    