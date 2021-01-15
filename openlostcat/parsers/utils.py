from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator
from openlostcat.operators.quantifier_operators import ANY

def is_bool_op(op):
    return issubclass(type(op), AbstractBoolOperator)

def is_bool_op_list(l):
    for op in l:
        if is_bool_op(op):
            return True
    return False

def get_as_bool_op(op, wrapper_bool_op = ANY):
    return op.wrap_as_bool_op(wrapper_bool_op) if not is_bool_op(op) else op

def get_as_bool_op_list(l, bool_op = ANY):
    return [get_as_bool_op(op, bool_op) for op in l]

