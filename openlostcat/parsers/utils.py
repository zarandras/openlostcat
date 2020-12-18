from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator

def is_bool_op(op):
    return issubclass(type(op), AbstractBoolOperator)

def is_bool_op_list(l):
    for op in l:
        if is_bool_op(op):
            return True
    return False

def get_as_bool_op(op, wrapper_bool_op):
    return op.wrap_as_bool_op(wrapper_bool_op) if not is_bool_op(op) else op

def get_as_bool_op_list(l, bool_op):
    return [get_as_bool_op(op, bool_op) for op in l]

# TODO
def choose_operator(op, filter_op_class, bool_op_class, check, getLogicalElement = lambda x: x):
    return bool_op_class(getLogicalElement(op)) if check(op) else filter_op_class(op)
