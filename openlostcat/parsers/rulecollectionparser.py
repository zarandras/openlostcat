from openlostcat.utils import error
from openlostcat.category import Category
from .opexpressionparser import OpExpressionParser
from openlostcat.parsers.refdict import RefDict

class RuleCollectionParser:
    """

    """
    
    def __init__(self, parserClass = OpExpressionParser, ref_dict = RefDict()):
        """

        :param parserClass:
        :param ref_dict:
        """
        self.ref_dict = ref_dict
        self.parser = parserClass(ref_dict)

    @staticmethod
    def __validate(category_rule_collection):
        """

        :param category_rule_collection:
        :return:
        """
        if not isinstance(category_rule_collection, dict) or "type" not in category_rule_collection or category_rule_collection["type"] != "CategoryRuleCollection" or \
        "categoryRules" not in category_rule_collection:
            return False
        return True

    @staticmethod
    def get_properties(category_rule_collection):
        """

        :param category_rule_collection:
        :return:
        """
        if "properties" not in category_rule_collection or not isinstance(category_rule_collection["properties"], dict):
            return {}
        return category_rule_collection["properties"]

    @staticmethod
    def __get_categoryRules(category_rule_collection):
        """

        :param category_rule_collection:
        :return:
        """
        return category_rule_collection["categoryRules"]
        
    def __parse_category_or_ref(self, source):
        """

        :param source:
        :return:
        """
        if not isinstance(source, dict):
            error("A category or reference definition must contain a JSON object: ", source)
        if len(source) > 1:
            error("A category or reference definition must have exactly one key-value pair: ", source)
        kv = next(iter(source.items()))
        if self.ref_dict.is_ref(kv[0]):
            ref_operator = self.parser.parse_operator(kv[1])
            self.ref_dict.set_ref(kv[0], ref_operator)
            return
        else:
            return Category(kv[0], kv[1], self.parser)

    def __parse_categories(self, cat):
        """

        :param cat:
        :return:
        """
        rule_switcher = {
            list: lambda l: [i for i in [self.__parse_category_or_ref(c) for c in l] if i],
            dict: lambda d: [i for i in [self.__parse_category_or_ref(d)] if i]
        }
        return rule_switcher.get(type(cat), error)(cat)
    
    def parseFile(self, category_rule_collection):
        """

        :param category_rule_collection:
        :return:
        """
        if self.__validate(category_rule_collection):
            return self.__parse_categories(self.__get_categoryRules(category_rule_collection))
        else:
            error("It is not a valid CategoryRuleCollection: ", category_rule_collection)