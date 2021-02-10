import unittest
from openlostcat.operators.filter_operators import AtomicFilter, FilterNOT
from openlostcat.operators.bool_operators import BoolNOT, BoolConst
from openlostcat.operators.quantifier_operators import ANY, ALL
from openlostcat.utils import to_tag_bundle_set


class TestNOTRules(unittest.TestCase):

    def testSimplyNot(self):
        self.assertTrue(BoolNOT(BoolConst(False)).apply(to_tag_bundle_set([]))[0])
        self.assertFalse(BoolNOT(BoolConst(True)).apply(to_tag_bundle_set([]))[0])

if __name__ == '__main__':
    unittest.main()


