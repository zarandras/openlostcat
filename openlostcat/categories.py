import json
from openlostcat.parsers.rulecollectionparser import RuleCollectionParser
from openlostcat.utils import error, indent, base_indent_num


class Categories:
    
    evaluationStrategy = "firstMatching"
    bool_ref_dict = {}
    filter_ref_dict = {}
    
    str_template = "Categories:\ncategory rule collection: [\n{categories}\n]"

    def __update_properties(self, prop):
        if 'evaluationStrategy' in prop:
            self.evaluationStrategy = prop['evaluationStrategy']

    def __init__(self, category_rule_collection, debug = False, parser = RuleCollectionParser()):
        self.debug = debug
        self.category_rule_collection = category_rule_collection
        if isinstance(self.category_rule_collection, str):
            with open(self.category_rule_collection) as f:
              self.category_rule_collection = json.load(f)
        self.properties = parser.get_properties(self.category_rule_collection)
        self.__update_properties(self.properties)
        self.parser = parser
        (self.categories, self.filter_ref_dict, self.bool_ref_dict) = parser.parseFile(self.category_rule_collection)
        
    def get_categories_enumerated_key_map(self):
        return dict(enumerate([c.name for c in self.categories]))
    
    def apply_fm_evaluation(self, tag_bundle_set):
        for num, category in enumerate(self.categories):
            (is_matching_category, op_result_meta_info) = category.apply(tag_bundle_set)
            if is_matching_category:
                return (num, category.name, op_result_meta_info)
        return (-1, None, [])
        
    def apply_all_evaluation(self, tag_bundle_set):
        categories_list = []
        for num, category in enumerate(self.categories):
            (is_matching_category, op_result_meta_info) = category.apply(tag_bundle_set)
            if is_matching_category:
                categories_list.append((num, category.name, op_result_meta_info))
        return categories_list if not categories_list else (-1, None, [])

    def apply(self, tag_bundle_set):
        evaluation_switcher = {
            "firstMatching" : self.apply_fm_evaluation,
            "all" : self.apply_all_evaluation
        }
        ret = evaluation_switcher.get(self.evaluationStrategy,
                               lambda x: error("Unsupported evaluation strategy: ", self.evaluationStrategy))(tag_bundle_set)
        return ret if self.debug else ret[:2]
        

    def __str__(self):
        return self.str_template.format(categories= 
                                   indent(
                                       '\n'.join([str(category) for category in self.categories]), 
                                       base_indent_num))
    