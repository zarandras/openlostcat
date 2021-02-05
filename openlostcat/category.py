from openlostcat.utils import indent, base_indent_num


class Category:
    """

    """

    str_template = "Category name: {name}\nrules: [\n{rules}\n]"
        
    def __init__(self, name, rules):
        """

        :param name:
        :param rules:
        """
        self.name = name
        self.rules = rules
    
    def apply(self, tag_bundle_set):
        """

        :param tag_bundle_set:
        :return:
        """
        return self.rules.apply(tag_bundle_set)

    def __str__(self):
        return self.str_template.format(name = self.name, rules= 
                                   indent(str(self.rules), base_indent_num))

