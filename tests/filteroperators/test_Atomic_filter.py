import unittest
from openlostcat.operators.filter_operators import AtomicFilter
from openlostcat.operators.quantifier_operators import ANY
from tests.filteroperators import test_set


class TestAtomicFilter(unittest.TestCase):

    def test_wrapper_quantifier_inheritance(self):
        """Test wrapper quantifier return value
        """
        self.assertEqual(AtomicFilter("key", "value").wrapper_quantifier, ANY)

    def test_bool_conversion(self):
        """Test Bool conversion to string feature
        """
        for b in [True, False]:
            with self.subTest(b=b):
                self.assertEqual(len(AtomicFilter("a", b).apply(test_set)), 1)

    def test_int_conversion(self):
        """Test int conversion to string feature
        """
        self.assertEqual(len(AtomicFilter("b", 2).apply(test_set)), 1)

    def test_exact_value(self):
        """Test string matching
        """
        self.assertEqual(len(AtomicFilter("c", "pass").apply(test_set)), 1)

    def test_list_value(self):
        """Test string matching
        """
        self.assertEqual(len(AtomicFilter("c", ["fail", "wont_pass"]).apply(test_set)), 2)

    def test_zero_matching(self):
        """Test non-matching set case
        """
        self.assertEqual(len(AtomicFilter("wont_match", ["fail", "wont_pass"]).apply(test_set)), 0)

    def test_zero_matching_for_zero_list(self):
        """Test the never-matching case
        """
        self.assertEqual(len(AtomicFilter("wont_match", []).apply(test_set)), 0)

    def test_error(self):
        """Test if exception is raised
        """
        for struct in [["fail"], {"fail"}]:
            with self.subTest(struct=struct):
                with self.assertRaises(SyntaxError):
                    AtomicFilter("c", [struct, "wont_pass"])

    def test_null_in_list(self):
        """Test null value functionality: makes the key optional (accepts the absence of the key as a match).
        """
        self.assertEqual(len(AtomicFilter("a", [None, True]).apply(test_set)), 3)

    def test_null_alone(self):
        """Test null-only value functionality: makes the key absent (no value is accepted as a match).
        """
        self.assertEqual(len(AtomicFilter("a", None).apply(test_set)), 2)


if __name__ == '__main__':
    unittest.main()
