from openlostcat.operators.bool_operators import BoolREF
from openlostcat.operators.quantifier_operators import ANY
from openlostcat.operators.filter_operators import FilterREF
from openlostcat.utils import error
from openlostcat.parsers.utils import get_as_bool_op, is_bool_op
from openlostcat.category import Category
from .opexpressionparser import OpExpressionParser

class RuleCollectionParser:
    
    def __init__(self, parserClass = OpExpressionParser, filter_ref_dict = {}, bool_ref_dict = {}):
        self.parserClass = parserClass
        self.filter_ref_dict = filter_ref_dict
        self.bool_ref_dict = bool_ref_dict

    @staticmethod
    def __validate(category_rule_collection):
        if not isinstance(category_rule_collection, dict) or "type" not in category_rule_collection or category_rule_collection["type"] != "CategoryRuleCollection" or \
        "categoryRules" not in category_rule_collection:
            return False
        return True

    @staticmethod
    def get_properties(category_rule_collection):
        if "properties" not in category_rule_collection or not isinstance(category_rule_collection["properties"], dict):
            return {}
        return category_rule_collection["properties"]

    @staticmethod
    def __get_categoryRules(category_rule_collection):
        return category_rule_collection["categoryRules"]

    @staticmethod
    def __is_ref(kv):
        return kv[0].startswith("#")

    @staticmethod
    def __is_bool_ref(kv):
        return kv[0].startswith("##")
        
    def __parse_category_or_ref(self, source):
        if not isinstance(source, dict):
            error("A category or reference definition must contain a JSON object: ", source)
        if len(source) > 1:
            error("A category or reference definition must have exactly one key-value pair: ", source)
        kv = next(iter(source.items()))
        if self.__is_ref(kv):
            op = self.parserClass(self.filter_ref_dict, self.bool_ref_dict).parse_operator(kv[1])
            if self.__is_bool_ref(kv):
                self.bool_ref_dict[kv[0]] = \
                    BoolREF(kv[0], op.wrap_as_bool_op(ANY) if not is_bool_op(op) else op)
            else:
                if is_bool_op(op):
                    error("Invalid reference definition. A bool expression is given but a filter expression is expected: ", op)
                self.filter_ref_dict[kv[0]] = FilterREF(kv[0], op)
                return
        else: 
            return Category(kv[0], kv[1], self.parserClass(self.filter_ref_dict, self.bool_ref_dict))

    def __parse_categories(self, cat):
        rule_switcher = {
            list: lambda l: [i for i in [self.__parse_category_or_ref(c) for c in l] if i],
            dict: lambda d: [i for i in [self.__parse_category_or_ref(d)] if i]
        }
        return rule_switcher.get(type(cat), error)(cat)
    
    def parseFile(self, category_rule_collection):
        if self.__validate(category_rule_collection):
            self.categories = self.__parse_categories(self.__get_categoryRules(category_rule_collection))
            return (self.categories, self.filter_ref_dict, self.bool_ref_dict)
        else:
            error("It is not a valid CategoryRuleCollection: ", category_rule_collection)