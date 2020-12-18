from .categories import Categories

class MainOsmCategorizer:

        def __init__(self, category_rule_collection, debug = False):
            """
            Provide Categories
            :param category_rule_collection: JSON structure as dictionary or file path
            :return: Categories
            """
            self.categories = Categories(category_rule_collection, debug = debug)

        def categorize(self, osm_json_dict):
            tag_bundle_set = [elements['tags'] for elements in osm_json_dict['elements'] if 'tags' in elements]
            return self.categories.apply(tag_bundle_set)
        
        def get_categories_enumerated_key_map(self):
            return self.categories.get_categories_enumerated_key_map()






