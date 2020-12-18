from .abstract_bool_operator import AbstractBoolOperator
from openlostcat.utils import error, indent, base_indent_num
    
class BoolAND(AbstractBoolOperator):
    
    str_template = "AND(\n{operators}\n)"
    
    def __init__(self, bool_operators):
        self.bool_operators = bool_operators
  
    def apply(self, tag_bundle_set):
        result_meta_info = []
        for op in self.bool_operators:
            (op_result, op_result_meta_info) = op.apply(tag_bundle_set)
            result_meta_info += self.prefix_meta_info_paths("FilterAND", op_result_meta_info)
            if not op_result:
                return (False, result_meta_info)
        return (True, result_meta_info)
    
    def __str__(self):
        return self.str_template.format(operators= 
                                   indent(
                                       '\n'.join([str(operator) for operator in self.bool_operators]),
                                       base_indent_num))
  
class BoolOR(AbstractBoolOperator):
    
    str_template = "OR[\n{operators}\n]"
    
    def __init__(self, bool_operators):
        self.bool_operators = bool_operators
  
    def apply(self, tag_bundle_set): 
        result_meta_info = []
        for op in self.bool_operators:
            (op_result, op_result_meta_info) = op.apply(tag_bundle_set)
            result_meta_info += self.prefix_meta_info_paths("FilterOR", op_result_meta_info)
            if op_result:
                return (True, result_meta_info)
        return (False, result_meta_info)
    
    def __str__(self):
        return self.str_template.format(operators= 
                                   indent(
                                       '\n'.join([str(operator) for operator in self.bool_operators]),
                                       base_indent_num))
  
class BoolNOT(AbstractBoolOperator):
    
    str_template = "NOT(\n{operator}\n)"
            
    def __init__(self, bool_operator):
        self.bool_operator = bool_operator
  
    def apply(self, tag_bundle_set): 
        (op_result, op_result_meta_info) = self.bool_operator.apply(tag_bundle_set)
        return (not op_result, self.prefix_meta_info_paths("FilterNOT", op_result_meta_info))
    
    def __str__(self):
        return self.str_template.format(operator= indent(str(self.bool_operator), base_indent_num))
    
    
class BoolREF(AbstractBoolOperator):
    
    str_template = "REF {name}(\n{operator}\n)"
    
    def __init__(self, name, bool_operator):
        self.name = name
        self.bool_operator = bool_operator
  
    def apply(self, tag_bundle_set): 
        return self.bool_operator.apply(tag_bundle_set)
    
    def __str__(self):
        return self.str_template.format(name= self.name, operator= indent(str(self.bool_operator), base_indent_num))
  
class BoolConst(AbstractBoolOperator):
    
    str_template = "CONST({const})"
  
    def __init__(self, const_val):
        self.const_val = const_val
  
    def apply(self, tag_bundle_set): 
        return (self.const_val, [str(self), tag_bundle_set])
    
    def __str__(self):
        return self.str_template.format(const=self.const_val)
    
# implication
class BoolIMPL(AbstractBoolOperator):
    
    str_template = "IMPL(\n{operators}\n)"
    
    def __init__(self, bool_operators):
        if len(bool_operators) < 2:
            error("Implication must contain at lest 2 elements :", bool_operators)
        self.bool_operators = bool_operators
        self.impl_op = BoolOR([BoolNOT(op) for op in bool_operators[:-1]] + [bool_operators[-1]])
        
  
    def apply(self, tag_bundle_set): 
        return self.impl_op.apply(tag_bundle_set)
    
    def __str__(self):
        return self.str_template.format(operators= 
                                   indent(
                                       '\n => \n'.join([str(operator) for operator in self.bool_operators]),
                                       base_indent_num))
