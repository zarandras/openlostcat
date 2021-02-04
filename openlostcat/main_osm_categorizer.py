from .categorycatalog import CategoryCatalog
from openlostcat.utils to_tag_bundle_set, get_tags_from_osm_elements

class MainOsmCategorizer:

        def __init__(self, category_rule_collection, debug = False):
            """
            Provide CategoryCatalog
            :param category_rule_collection: JSON structure as dictionary or file path
            :return: CategoryCatalog
            """
            self.category_cat = CategoryCatalog(category_rule_collection, debug = debug)

        def categorize(self, osm_json_dict):
            tag_bundle_set = to_tag_bundle_set(get_tags_from_osm_elements(osm_json_dict))
            return self.category_cat.apply(tag_bundle_set)
        
        def get_categories_enumerated_key_map(self):
            return self.category_cat.get_categories_enumerated_key_map()

        def __str__(self):
            return str(self.category_cat)






