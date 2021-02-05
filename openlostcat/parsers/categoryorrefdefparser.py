from openlostcat.utils import error
from openlostcat.category import Category
from .opexpressionparser import OpExpressionParser
from openlostcat.parsers.refdict import RefDict
from openlostcat.operators.bool_operators import BoolOR
from openlostcat.operators.abstract_filter_operator import AbstractFilterOperator


class CategoryOrRefDefParser:
    """

    """

    def __init__(self, op_exp_parser = OpExpressionParser(), ref_dict = RefDict()):
        """

        :param op_exp_parser:
        :param ref_dict:
        """
        self.op_exp_parser = op_exp_parser
        self.op_exp_parser.set_ref_dict(ref_dict)

    def get_ref_dict(self):
        return self.op_exp_parser.get_ref_dict()

    def set_ref_dict(self, ref_dict):
        self.op_exp_parser.set_ref_dict(ref_dict)


    def parse(self, source):
        """

        :param source:
        :return:
        """
        if not isinstance(source, dict):
            error("A category or reference definition must contain a JSON object: ", source)
        if len(source) > 1:
            error("A category or reference definition must have exactly one key-value pair: ", source)
        kv = next(iter(source.items()))
        if RefDict.is_ref(kv[0]):
            ref_operator = self.op_exp_parser.parse(kv[1])
            return RefDict.create_ref(kv[0], ref_operator)
        else:
            return Category(kv[0], self.parse_category_rules(kv[1]))




    def parse_category_rules(self, rules):
        """

        :param rules:
        :return:
        """
        if isinstance(rules, list):
            # A category-level list is interpreted as a list of bool level rules
            # (each item forced as a bool op instead of a filter-or)
            return BoolOR(AbstractFilterOperator.get_as_bool_op_list([self.op_exp_parser.parse(r) for r in rules]))
        else:
            # Any other json element as category is interpreted as a single bool-level operator
            # (any filter-level ops forced as bool ops by wrapping them into an ANY quantifier)
            return AbstractFilterOperator.get_as_bool_op(self.op_exp_parser.parse(rules))