import unittest
from openlostcat.operators.filter_operators import AtomicFilter, FilterNOT, FilterConst
from openlostcat.operators.bool_operators import BoolNOT
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.utils import to_tag_bundle_set


class TestQuantifier(unittest.TestCase):
    tests = [
        [
            {
                "landuse": "residential",
                "highway": "motorway",
                "surface": "BAD"
            },
            {
                "landuse": "residential",
                "highway": "motorway"
            }
        ],
        [
            {
                "landuse": "residential",
                "highway": "motorway",
                "surface": "BAD"
            },
            {
                "landuse": "residential",
                "highway": "motorway"
            },
            {
                "landuse": "BAD",
                "highway": "motorway"
            }
        ],
        [
            {
                "landuse": "residential",
                "highway": "BAD",
                "surface": "asphalt"
            },
            {
                "landuse": "residential",
                "highway": "motorway",
                "surface": "asphalt"
            },
            {
                "landuse": "residential",
                "highway": "motorway",
                "surface": "asphalt"
            },
            {
                "landuse": "residential",
                "highway": "motorway",
                "surface": "BAD"
            },
            {
                "landuse": "residential",
                "highway": "motorway"
            },
            {
                "landuse": "BAD",
                "highway": "motorway"
            }
        ]
    ]

    boolnot_all = BoolNOT(ALL(None, AtomicFilter("landuse", "residential")))
    any_filternot = ANY(None, FilterNOT(AtomicFilter("landuse", "residential")))

    all_filternot = ALL(None, FilterNOT(AtomicFilter("landuse", "residential")))
    boolnot_any = BoolNOT(ANY(None, AtomicFilter("landuse", "residential")))

    def test_filter_and_bool_Not_connection(self):
        for test in self.tests:
            self.assertTrue(
                self.boolnot_all.apply(to_tag_bundle_set(test))[0] ==
                self.any_filternot.apply(to_tag_bundle_set(test))[0])
            self.assertTrue(
                self.all_filternot.apply(to_tag_bundle_set(test))[0] ==
                self.boolnot_any.apply(to_tag_bundle_set(test))[0])

    def test_simply_ANY_ALL(self):
        self.assertFalse(ANY(None, FilterConst(False)).apply(to_tag_bundle_set([{"foo": "void"}]))[0])
        self.assertFalse(ALL(None, FilterConst(False)).apply(to_tag_bundle_set([{"foo": "void"}]))[0])
        self.assertTrue(ANY(None, FilterConst(True)).apply(to_tag_bundle_set([{"foo": "void"}]))[0])
        self.assertTrue(ALL(None, FilterConst(True)).apply(to_tag_bundle_set([{"foo": "void"}]))[0])


if __name__ == '__main__':
    unittest.main()
