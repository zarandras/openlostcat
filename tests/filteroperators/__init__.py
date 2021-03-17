from openlostcat.utils import to_tag_bundle_set
from openlostcat.operators.filter_operators import FilterConst

test_set = to_tag_bundle_set([
    {
        "a": "yes",
        "c": "fail",
        "d": "pass",
        "e": "fail"
    },
    {
        "a": "no",
        "b": "2",
        "d": "fail",
        "e": "pass"
    },
    {
        "c": "pass",
        "d": "pass",
        "e": "pass"
    },
    {
        "c": "fail"
    }
])

test_operators_list = [
    [FilterConst(False), FilterConst(True)],
    [FilterConst(True), FilterConst(False)],
    [FilterConst(True), FilterConst(True)],
    [FilterConst(False), FilterConst(False)],
    [FilterConst(False), FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True)],
    [FilterConst(True), FilterConst(False), FilterConst(False), FilterConst(False), FilterConst(False)],
    [FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True), FilterConst(True)],
    [FilterConst(False), FilterConst(False), FilterConst(False), FilterConst(False), FilterConst(False)]
]

test_tag_bundle_set = to_tag_bundle_set([{"foo": "void"}])
