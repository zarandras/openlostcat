from .abstract_bool_operator import AbstractBoolOperator
from openlostcat.utils import indent, base_indent_num
# from openlostcat.parsers.utils import  is_bool_op
from openlostcat.utils import error

class ALL(AbstractBoolOperator):
    
    str_template = "ALL(\n{operator}\n)"
            
    def __init__(self, name, operator):
        if self.is_bool_op(operator):
            error("ALL is not defined for logical operators", operator)
        self.filter_operator = operator
        self.name = self.get_name("__ALL", name)
        
             
    def apply(self, tag_bundle_set):
        matching_tag_bundles = self.filter_operator.apply(tag_bundle_set)
        return (len(matching_tag_bundles) == len(tag_bundle_set), [(self.name, matching_tag_bundles)])
    
    def __str__(self):
        return self.str_template.format(operator= indent(str(self.filter_operator), base_indent_num))


class ANY(AbstractBoolOperator):
    
    str_template = "ANY(\n{operator}\n)"
            
    def __init__(self, name, operator):
        if self.is_bool_op(operator):
            error("ANY is not defined for logical operators", operator)
        self.filter_operator = operator
        self.name = self.get_name("__ANY", name)
  
    def apply(self, tag_bundle_set):
        matching_tag_bundles = self.filter_operator.apply(tag_bundle_set)
        return (len(matching_tag_bundles) > 0, [(self.name, matching_tag_bundles)])
    
    def __str__(self):
        return self.str_template.format(operator= indent(str(self.filter_operator), base_indent_num))