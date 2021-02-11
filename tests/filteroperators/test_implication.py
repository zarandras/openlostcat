import unittest

from openlostcat.operators.filter_operators import AtomicFilter, FilterIMPL, FilterConst, FilterNOT, FilterOR
from openlostcat.operators.quantifier_operators import ALL
from openlostcat.utils import to_tag_bundle_set


class TestImpl(unittest.TestCase):
    test = to_tag_bundle_set([
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
    ])

    s1 = AtomicFilter("landuse", "residential")
    s2 = AtomicFilter("highway",
                      ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential"])
    s3 = AtomicFilter("surface", ["paved", "asphalt", "concrete"])

    def testWith2parameter(self):
        impl1 = FilterIMPL([self.s2, self.s3])
        self.assertTrue(
            not impl1.apply(self.test) - to_tag_bundle_set([
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ])
        )
        self.assertTrue(
            not to_tag_bundle_set([
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ]) - impl1.apply(self.test)
        )

    def testWith3parameter(self):
        impl2 = FilterIMPL([self.s1, self.s2, self.s3])
        self.assertTrue(
            not impl2.apply(self.test) - to_tag_bundle_set([
                    {'landuse': 'BAD', 'highway': 'motorway'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ])
        )
        self.assertTrue(
            not to_tag_bundle_set([
                    {'landuse': 'BAD', 'highway': 'motorway'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ]) - impl2.apply(self.test)
        )

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

    @staticmethod
    def implication_as_operators(bool_const_operators):
        return FilterOR([FilterNOT(op) for op in bool_const_operators[:-1]] + [bool_const_operators[-1]])

    test_tag_bundle_set = [{"foo": "void"}]

    def test_implication_equivalence(self):
        for test_operators in self.test_operators_list:
            self.assertEqual(FilterIMPL(test_operators).apply(to_tag_bundle_set(self.test_tag_bundle_set)),
                             TestImpl.implication_as_operators(test_operators).
                             apply(to_tag_bundle_set(self.test_tag_bundle_set)))

    def test_wrapper_quantifier_inheritance(self):
        self.assertEqual(FilterIMPL([FilterConst(False), FilterConst(True)]).wrapper_quantifier, ALL)


if __name__ == '__main__':
    unittest.main()
