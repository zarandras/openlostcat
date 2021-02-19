import unittest
from openlostcat.operators.filter_operators import AtomicFilter
from openlostcat.operators.quantifier_operators import ANY
from openlostcat.utils import to_tag_bundle_set


class TestAtomicFilter(unittest.TestCase):

    test_set = to_tag_bundle_set([
        {
            "a": "yes",
            "c": "fail"
        },
        {
            "a": "no",
            "b": "2"
        },
        {
            "c": "pass"
        }
    ])

    def test_wrapper_quantifier_inheritance(self):
        self.assertEqual(AtomicFilter("key", "value").wrapper_quantifier, ANY)

    def test_bool_conversion(self):
        """
        Test the Bool conversation to string feature
        """
        for b in [True, False]:
            with self.subTest(b=b):
                self.assertEqual(len(AtomicFilter("a", b).apply(self.test_set)), 1)

    def test_int_conversion(self):
        """
        Test the int conversation to string feature
        """
        self.assertEqual(len(AtomicFilter("b", 2).apply(self.test_set)), 1)

    def test_exact_value(self):
        """
        Test string matching
        """
        self.assertEqual(len(AtomicFilter("c", "pass").apply(self.test_set)), 1)

    def test_list_value(self):
        """
        Test string matching
        """
        self.assertEqual(len(AtomicFilter("c", ["fail", "wont_pass"]).apply(self.test_set)), 1)

    def test_error(self):
        """
        Test if exception is raised
        """
        for struct in [["fail"], {"fail"}]:
            with self.subTest(struct=struct):
                with self.assertRaises(SyntaxError):
                    AtomicFilter("c", [struct, "wont_pass"])


if __name__ == '__main__':
    unittest.main()
