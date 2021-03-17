import unittest

from openlostcat.operators.filter_operators import AtomicFilter
from openlostcat.operators.bool_operators import BoolIMPL, BoolOR, BoolNOT, BoolConst
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.utils import to_tag_bundle_set


class TestImpl(unittest.TestCase):
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

    s1 = ALL(None, AtomicFilter("landuse", "residential"))
    s2 = ALL(None, AtomicFilter("highway", ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified",
                                            "residential"]))
    s3 = ANY(None, AtomicFilter("surface", ["paved", "asphalt", "concrete"]))

    def test_with_2parameters(self):
        impl1 = BoolIMPL([self.s2, self.s3])
        validation = [False, False, True]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(impl1.apply(to_tag_bundle_set(test))[0], valid)

    def test_with_3parameters(self):
        impl2 = BoolIMPL([self.s1, self.s2, self.s3])
        validation = [False, True, True]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(impl2.apply(to_tag_bundle_set(test))[0], valid)

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

    @staticmethod
    def implication_as_operators(bool_const_operators):
        return BoolOR([BoolNOT(op) for op in bool_const_operators[:-1]] + [bool_const_operators[-1]])

    def test_implication_equivalence(self):
        for test_operators in self.test_operators_list:
            self.assertEqual(BoolIMPL(test_operators).apply(to_tag_bundle_set([]))[0],
                             TestImpl.implication_as_operators(test_operators).apply(to_tag_bundle_set([]))[0])


if __name__ == '__main__':
    unittest.main()
