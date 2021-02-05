from openlostcat.utils import error
from openlostcat.operators.filter_operators import FilterAND, FilterOR, FilterNOT, AtomicFilter, FilterIMPL
from openlostcat.operators.bool_operators import BoolAND, BoolOR, BoolNOT, BoolConst, BoolIMPL
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.parsers.refdict import RefDict
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator
from openlostcat.operators.abstract_filter_operator import AbstractFilterOperator
import re


class OpExpressionParser:
    """

    """
    
    def __init__(self, ref_dict = RefDict()):
        """

        :param ref_dict:
        """
        self.ref_dict = ref_dict


    def get_ref_dict(self):
        return self.ref_dict

    def set_ref_dict(self, ref_dict):
        self.ref_dict = ref_dict

    @staticmethod
    def __create_multiary_operator(op_list, filter_op_class, bool_op_class):
        """

        :param op_list:
        :param filter_op_class:
        :param bool_op_class:
        :return:
        """
        return bool_op_class(AbstractFilterOperator.get_as_bool_op_list(op_list)) if AbstractBoolOperator.is_bool_op_list(op_list) else filter_op_class(op_list)

    op_list_len_check = lambda self, x: len(x) == 1
    
    def __create_or(self, l):
        return self.__parse_standalone_operator(l[0]) if self.op_list_len_check(l) else  self.__create_multiary_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterOR, BoolOR)

    def __create_and(self, d):
        return self.__parse_keyvalue_operator(*next(iter(d.items()))) if self.op_list_len_check(d) else  self.__create_multiary_operator(
            [self.__parse_keyvalue_operator(*t) for t in d.items()],
            FilterAND, BoolAND)
    
    def __create_impl(self, l):
        return self.__create_multiary_operator(
            [self.__parse_standalone_operator(e) for e in l],
            FilterIMPL, BoolIMPL)

    def __create_not(self, source):
        create_unary_operator = lambda op, filter_op_class, bool_op_class: bool_op_class(op) \
            if AbstractBoolOperator.is_bool_op(op) else filter_op_class(op)
        return create_unary_operator(self.__parse_standalone_operator(source),
                FilterNOT, BoolNOT)

    @staticmethod
    def __get_operator_prefix(key_str):
        """

        :param key_str:
        :return:
        """
        try:
            return re.findall("^__([^_]*)_", key_str)[0]
        except IndexError:
            return ""

    @staticmethod
    def __check_json_type(source, type_list):
        """

        :param source:
        :param type_list:
        :return:
        """
        return any(isinstance(source, type_candidate) for type_candidate in type_list)

    def __parse_keyvalue_operator(self, k, v):
        """

        :param k:
        :param v:
        :return:
        """
        create_and_check =lambda x, create_fv, type_list, error_message : create_fv(x) \
            if self.__check_json_type(x, type_list) \
            else error(error_message, x)
        switcher = {
            "OR":   lambda x:  create_and_check(x, self.__create_or, [list], "__OR_ key must contain a list element"),
            "AND":  lambda x:  create_and_check(x, self.__create_and, [dict], "__AND_ key must contain a dict element"),
            "NOT":  lambda x:  create_and_check(x, self.__create_not, [list, dict], "__NOT_ must contain a list or dict elements"),
            "REF":  lambda x:  create_and_check(x, self.ref_dict.get_ref, [str], "__REF_ must contain a string elements"),
            "IMPL": lambda x:  create_and_check(x, self.__create_impl, [list], "__IMPL_ key must contain a list element"),
            "BOOLCONST": BoolConst,
            "ANY": lambda x:  ANY(k, self.__parse_standalone_operator(x)),
            "ALL": lambda x:  ALL(k, self.__parse_standalone_operator(x))
        }
        return switcher.get(self.__get_operator_prefix(k), lambda x:  AtomicFilter(k, x))(v)

    def __parse_standalone_operator(self, source):
        """For JSON items without attribute name (key)

        :param source:
        :return:
        """
        switcher = {
            list: self.__create_or,
            dict: self.__create_and,
            str: self.ref_dict.get_ref,
            bool: BoolConst
        }
        return switcher.get(type(source),
                            lambda x: error("Atomic value is not allowed here: ", x))(source)
    
    def parse(self, source):
        """

        :param source:
        :return:
        """
        return self.__parse_standalone_operator(source)
    