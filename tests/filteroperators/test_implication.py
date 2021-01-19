import unittest

from openlostcat.operators.filter_operators import AtomicFilter, FilterIMPL


class TestIMPL(unittest.TestCase):
    test = [
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

    s1 = AtomicFilter("landuse", "residential")
    s2 = AtomicFilter("highway", ["motorway", "trunk", "primary", "secondary", "tertiary", "unclassified", "residential"])
    s3 = AtomicFilter("surface", ["paved", "asphalt", "concrete"])

    def testWith2parameter(self):
        impl1 = FilterIMPL([self.s2, self.s3])
        self.assertTrue(
            not impl1.tag_bundle_set_diff(
                impl1.apply(self.test),
                [
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'}, 
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ]
            ) 
        )
        self.assertTrue(
            not impl1.tag_bundle_set_diff(
                [
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'}, 
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ],
                impl1.apply(self.test)
            ) 
        )
        
    def testWith3parameter(self):
        impl2 = FilterIMPL([self.s1, self.s2, self.s3])
        self.assertTrue(
            not impl2.tag_bundle_set_diff(
                impl2.apply(self.test),
                [
                    {'landuse': 'BAD', 'highway': 'motorway'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'}, 
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ]
            ) 
        )
        self.assertTrue(
            not impl2.tag_bundle_set_diff(
                [
                    {'landuse': 'BAD', 'highway': 'motorway'},
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'BAD'}, 
                    {'surface': 'asphalt', 'landuse': 'residential', 'highway': 'motorway'}
                ],
                impl2.apply(self.test)
            ) 
        )

if __name__ == '__main__':
    unittest.main()