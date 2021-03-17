"""
Quantifier operators bridge between set(filter)-level subexpressions and category(bool)-level subexpressions
by quantifying the filtered result set into a single bool value.
"""
from .abstract_bool_operator import AbstractBoolOperator
from openlostcat.utils import indent, base_indent_num
from openlostcat.utils import error


class ALL(AbstractBoolOperator):
    """Universal quantifier - returns True if the filter subexpression equals to its given operand (all elements match)

    """

    str_template = "ALL[{name}](\n{operator}\n)"
            
    def __init__(self, name, operator):
        if self.is_bool_op(operator):
            error("ALL is not defined for bool operators: ", operator)
        self.filter_operator = operator
        self.name = self.get_name("__ALL_", name, self.filter_operator)

    def apply(self, tag_bundle_set):
        matching_tag_bundles = self.filter_operator.apply(tag_bundle_set)
        return len(matching_tag_bundles) == len(tag_bundle_set), [(self.name, matching_tag_bundles)]
    
    def __str__(self):
        return self.str_template.format(name=self.name[6:],
                                        operator=indent(str(self.filter_operator), base_indent_num))


class ANY(AbstractBoolOperator):
    """Existential quantifier - returns True if the filter subexpression is nonempty (any of the elements match)

    """
    
    str_template = "ANY[{name}](\n{operator}\n)"
            
    def __init__(self, name, operator):
        if self.is_bool_op(operator):
            error("ANY is not defined for bool operators: ", operator)
        self.filter_operator = operator
        self.name = self.get_name("__ANY_", name, self.filter_operator)
  
    def apply(self, tag_bundle_set):
        matching_tag_bundles = self.filter_operator.apply(tag_bundle_set)
        return len(matching_tag_bundles) > 0, [(self.name, matching_tag_bundles)]

    def __str__(self):
        return self.str_template.format(name=self.name[6:],
                                        operator=indent(str(self.filter_operator), base_indent_num))
