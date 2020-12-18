import unittest
from openlostcat.operators.filter_operators import AtomicFilter, FilterNOT
from openlostcat.operators.bool_operators import BoolNOT
from openlostcat.operators.quantifier_operators import ANY, ALL


class TestNOTRules(unittest.TestCase):
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


    s1 = BoolNOT(ALL(None, AtomicFilter("landuse", "residential")))
    s2 = ANY(None, FilterNOT(AtomicFilter("landuse", "residential")))

    s3 = ALL(None, FilterNOT(AtomicFilter("landuse", "residential")))
    s4 = BoolNOT(ANY(None, AtomicFilter("landuse", "residential")))

    def testNotRule(self):
        for test in self.tests:
            self.assertTrue(self.s1.apply(test)[0] == self.s2.apply(test)[0])
            self.assertTrue(self.s3.apply(test)[0] == self.s4.apply(test)[0])


if __name__ == '__main__':
    unittest.main()


