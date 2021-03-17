from openlostcat.operators.bool_operators import BoolConst

test_operators_list = [
    [BoolConst(False), BoolConst(True)],
    [BoolConst(True), BoolConst(False)],
    [BoolConst(True), BoolConst(True)],
    [BoolConst(False), BoolConst(False)],
    [BoolConst(False), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True)],
    [BoolConst(True), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False)],
    [BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True), BoolConst(True)],
    [BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False), BoolConst(False)]
]

test_operators_list_simple = [
    [BoolConst(False), BoolConst(True)],
    [BoolConst(True), BoolConst(False)],
    [BoolConst(True), BoolConst(True)],
    [BoolConst(False), BoolConst(False)]
]