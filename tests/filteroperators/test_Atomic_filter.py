import unittest
from openlostcat.operators.filter_operators import AtomicFilter
from openlostcat.operators.quantifier_operators import ANY
# from openlostcat.utils import to_tag_bundle_set


class TestAtomicFilter(unittest.TestCase):

    def test_wrapper_quantifier_inheritance(self):
        self.assertEqual(AtomicFilter("key", "value").wrapper_quantifier, ANY)


if __name__ == '__main__':
    unittest.main()
