from openlostcat.utils import to_tag_bundle_set, get_tags_from_osm_elements
from openlostcat.parsers.categorycatalogparser import CategoryCatalogParser

class MainOsmCategorizer:
    """

    """

    def __init__(self, category_action_representation, debug = False, category_catalog_parser = CategoryCatalogParser()):
        """

        :param category_action_representation: JSON structure as dictionary or file path
        :param debug:
        :param category_catalog_parser:
        """
        self.category_cat = category_catalog_parser.parse(category_action_representation, debug = debug)

    def categorize(self, osm_json_dict):
        """

        :param osm_json_dict:
        :return:
        """
        tag_bundle_set = to_tag_bundle_set(get_tags_from_osm_elements(osm_json_dict))
        return self.category_cat.apply(tag_bundle_set)

    def get_categories_enumerated_key_map(self):
        """

        :return:
        """
        return self.category_cat.get_categories_enumerated_key_map()

    def __str__(self):
        return str(self.category_cat)






