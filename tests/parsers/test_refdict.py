import unittest
from openlostcat.operators.filter_operators import FilterConst, FilterREF
from openlostcat.operators.bool_operators import BoolConst, BoolREF
from openlostcat.parsers.refdict import RefDict


class TestRefDict(unittest.TestCase):

    def test_is_ref(self):
        """Test is_ref function
        """
        self.assertTrue(RefDict.is_ref("#filter_ref"))
        self.assertTrue(RefDict.is_ref("##bool_ref"))
        self.assertFalse(RefDict.is_ref("not_a_valid_ref"))

    def test_is_bool_ref(self):
        """Test is_bool_ref function
        """
        self.assertFalse(RefDict.is_bool_ref("#filter_ref"))
        self.assertTrue(RefDict.is_bool_ref("##bool_ref"))
        self.assertFalse(RefDict.is_bool_ref("not_a_valid_ref"))

    def test_create_ref(self):
        """Test create_ref function
        """
        with self.assertRaises(SyntaxError):
            RefDict.create_ref("not_a_valid_ref", FilterConst(False))
        with self.assertRaises(SyntaxError):
            RefDict.create_ref("#filter_ref", BoolConst(False))
        self.assertTrue(isinstance(RefDict.create_ref("#filter_ref", FilterConst(True)), FilterREF))
        self.assertTrue(isinstance(RefDict.create_ref("##bool_ref", BoolConst(True)), BoolREF))
        self.assertTrue(isinstance(RefDict.create_ref("##bool_ref", FilterConst(True)), BoolREF))

    def test_getter_setter_filter(self):
        """Test get and set function
        """
        filter_ref = RefDict.create_ref("#filter_ref", FilterConst(True))
        ref_dict = RefDict()
        ref_dict.set_ref(filter_ref)
        self.assertEqual(len(ref_dict.filter_ref_dict), 1)
        self.assertEqual(ref_dict.get_ref("#filter_ref"), filter_ref)

    def test_getter_setter_bool(self):
        """Test get and set function
        """
        bool_ref = RefDict.create_ref("##bool_ref", BoolConst(True))
        ref_dict = RefDict()
        ref_dict.set_ref(bool_ref)
        self.assertEqual(len(ref_dict.bool_ref_dict), 1)
        self.assertEqual(ref_dict.get_ref("##bool_ref"), bool_ref)


if __name__ == '__main__':
    unittest.main()
