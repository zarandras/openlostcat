from openlostcat.utils import indent, base_indent_num


class Category:
    """Represents a single place category defined by its rules for osm tags

    """

    str_template = "Category name: {name}\nrules: [\n{rules}\n]"
        
    def __init__(self, name, rules):
        """Initializes a category with rules

        :param name: string
        :param rules: AbstractBoolOperator (usually a BoolOr if multiple rules are given)
        """
        self.name = name
        self.rules = rules
    
    def apply(self, tag_bundle_set):
        """Determines whether a location belongs to this category or not

        :param tag_bundle_set: a set of tag bundles of osm elements at the location
        :return: boolean whether the rules of this category are true for the given location
        """
        return self.rules.apply(tag_bundle_set)

    def __str__(self):
        return self.str_template.format(name=self.name, rules=indent(str(self.rules), base_indent_num))
