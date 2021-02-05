import json
from openlostcat.parsers.categorycatalogparser import CategoryCatalogParser
from openlostcat.utils import error, indent, base_indent_num


class CategoryCatalog:
    """

    """
    
    evaluationStrategy = "firstMatching"
    """evaluationStrategy  """
    
    str_template = "CategoryCatalog:\ncategory rule collection: [\n{categories}\n]"

    def __update_properties(self, prop):
        if 'evaluationStrategy' in prop:
            self.evaluationStrategy = prop['evaluationStrategy']

    def __init__(self, category_rule_collection, debug = False, parser = CategoryCatalogParser()):
        """

        :param category_rule_collection:
        :param debug:
        :param parser:
        """
        self.debug = debug
        if isinstance(category_rule_collection, str):
            with open(category_rule_collection) as f:
              category_rule_collection = json.load(f)
        self.properties = parser.get_properties(category_rule_collection)
        self.__update_properties(self.properties)
        self.categories = parser.parseFile(category_rule_collection)
        
    def get_categories_enumerated_key_map(self):
        """

        :return:
        """
        return dict(enumerate([c.name for c in self.categories]))
    
    def apply_fm_evaluation(self, tag_bundle_set):
        """

        :param tag_bundle_set:
        :return:
        """
        for num, category in enumerate(self.categories):
            (is_matching_category, op_result_meta_info) = category.apply(tag_bundle_set)
            if is_matching_category:
                return (num, category.name, op_result_meta_info) if self.debug else (num, category.name)
        return (-1, None, []) if self.debug else (-1, None)
        
    def apply_all_evaluation(self, tag_bundle_set):
        """

        :param tag_bundle_set:
        :return:
        """
        categories_list = []
        for num, category in enumerate(self.categories):
            (is_matching_category, op_result_meta_info) = category.apply(tag_bundle_set)
            if is_matching_category:
                categories_list.append((num, category.name, op_result_meta_info) if self.debug else (num, category.name))
        return categories_list if categories_list else [(-1, None, []) if self.debug else (-1, None)]

    def apply(self, tag_bundle_set):
        """
        
        :param tag_bundle_set:
        :return:
        """
        evaluation_switcher = {
            "firstMatching" : self.apply_fm_evaluation,
            "all" : self.apply_all_evaluation
        }
        return evaluation_switcher.get(self.evaluationStrategy,
                               lambda x: error("Unsupported evaluation strategy: ", self.evaluationStrategy))(tag_bundle_set)
        

    def __str__(self):
        return self.str_template.format(categories= 
                                   indent(
                                       '\n'.join([str(category) for category in self.categories]), 
                                       base_indent_num))
    