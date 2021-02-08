from openlostcat.utils import error
from openlostcat.category import Category
from openlostcat.categorycatalog  import CategoryCatalog
from openlostcat.parsers.refdict import RefDict
from .categoryorrefdefparser import CategoryOrRefDefParser

class CategoryCatalogParser:
    """

    """

    category_rule_collection_type = "CategoryRuleCollection"
    """
    """

    category_rules_key = "categoryRules"
    """
    """

    properties_key = "properties"
    """
    """


    
    def __init__(self, category_or_refdef_parser = CategoryOrRefDefParser(), ref_dict = RefDict()):
        """

        :param category_or_refdef_parser:
        :param ref_dict:
        """
        self.ref_dict = ref_dict
        self.category_or_refdef_parser = category_or_refdef_parser
        self.category_or_refdef_parser.set_ref_dict(self.ref_dict)


    def validate(self, category_rule_collection):
        """

        :param category_rule_collection:
        :return:
        """
        if not isinstance(category_rule_collection, dict) or "type" not in category_rule_collection or category_rule_collection["type"] != self.category_rule_collection_type or \
        self.category_rules_key not in category_rule_collection:
            return False
        return True

    def get_properties(self, category_rule_collection):
        """

        :param category_rule_collection:
        :return:
        """
        if self.properties_key not in category_rule_collection or not isinstance(category_rule_collection[self.properties_key], dict):
            return {}
        return category_rule_collection[self.properties_key]

    def __get_category_rules(self, category_action_representation):
        """

        :param category_action_representation:
        :return:
        """
        return category_action_representation[self.category_rules_key]


    def __get_category_list(self, category_rules):
        """

        :param category_rules:
        :return:
        """
        res = []
        for source in category_rules:
            cat_or_ref = self.category_or_refdef_parser.parse(source)
            if isinstance(cat_or_ref, Category):
                res.append(cat_or_ref)
            else:
                self.ref_dict.set_ref(cat_or_ref)
        return res
    
    def check_and_parse_category_list(self, category_action_representation):
        """

        :param category_action_representation:
        :return:
        """
        if not self.validate(category_action_representation):
            error("It is not a valid CategoryRuleCollection: ", category_action_representation)
        category_rules = self.__get_category_rules(category_action_representation)
        rule_switcher = {
            list: lambda l: l,
            dict: lambda d: [d]
        }
        return self.__get_category_list(rule_switcher.get(type(category_rules), error)(category_rules))

        # def parseFile(self, category_rule_collection):
        #     """
        #
        #     :param category_rule_collection:
        #     :return:
        #     """
        # if not self.validate(category_rule_collection):
        #     error("It is not a valid CategoryRuleCollection: ", category_rule_collection)
        # category_rules = self.__get_category_rules(category_rule_collection)
        # rule_switcher = {
        #     list: lambda l: self.__get_category_list(l),
        #     dict: lambda d: self.__get_category_list([d])
        # }
        # return rule_switcher.get(type(category_rules), error)(category_rules)


    def parse(self, category_action_representation, debug = False):
        """Provide CategoryCatalog

        :param category_action_representation: JSON structure as dictionary or file path
        :param debug:
        :return:
        """
        if isinstance(category_action_representation, str):
            with open(category_action_representation) as f:
                category_action_representation = json.load(f)
        category_cat = CategoryCatalog(self.check_and_parse_category_list(category_action_representation), debug)
        category_cat.update_properties(self.get_properties(category_action_representation))
        return category_cat

