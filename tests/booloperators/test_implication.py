import unittest

from openlostcat.operators.filter_operators import AtomicFilter
from openlostcat.operators.bool_operators import BoolIMPL
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.utils import to_tag_bundle_set


class TestIMPL(unittest.TestCase):
    tests = [
        [
            {
                "landuse" : "residential",
                "highway" : "motorway",
                "surface" : "BAD"
            },
            {
                "landuse" : "residential",
                "highway" : "motorway"
            }
        ],
        [
            {
                "landuse" : "residential",
                "highway" : "motorway",
                "surface" : "BAD"
            },
            {
                "landuse" : "residential",
                "highway" : "motorway"
            },
            {
                "landuse" : "BAD",
                "highway" : "motorway"
            }
        ],
        [
            {
               "landuse" : "residential",
               "highway" : "BAD",
               "surface" : "asphalt"
            },
            {
               "landuse" : "residential",
               "highway" : "motorway",
               "surface" : "asphalt"
            },
            {
               "landuse" : "residential",
               "highway" : "motorway",
               "surface" : "asphalt"
            },
            {
                "landuse" : "residential",
                "highway" : "motorway",
                "surface" : "BAD"
            },
            {
                "landuse" : "residential",
                "highway" : "motorway"
            },
            {
                "landuse" : "BAD",
                "highway" : "motorway"
            }
        ]
    ]

    s1 = ALL(None, AtomicFilter("landuse", "residential"))
    s2 = ALL(None, AtomicFilter("highway", ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential"]))
    s3 = ANY(None, AtomicFilter("surface", ["paved", "asphalt", "concrete"]))

    def testWith2parameter(self):
        impl1 = BoolIMPL([self.s2, self.s3])
        validation = [False, False, True]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(impl1.apply(to_tag_bundle_set(test))[0], valid)
        
    def testWith3parameter(self):
        impl2 = BoolIMPL([self.s1, self.s2, self.s3])
        validation = [False, True, True]
        for (test, valid) in list(zip(self.tests, validation)):
            self.assertEqual(impl2.apply(to_tag_bundle_set(test))[0], valid)

if __name__ == '__main__':
    unittest.main()