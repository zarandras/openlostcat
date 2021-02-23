import unittest
from openlostcat.operators.filter_operators import FilterConst, FilterREF
from openlostcat.operators.bool_operators import BoolConst, BoolREF
from openlostcat.parsers.refdict import RefDict

from openlostcat.parsers.opexpressionparser import OpExpressionParser
from openlostcat.parsers.categoryorrefdefparser import CategoryOrRefDefParser
from openlostcat.parsers.categorycatalogparser import CategoryOrRefDefParser


from unittest.mock import patch
from unittest.mock import MagicMock


class TestParserProcess(unittest.TestCase):

    @patch('openlostcat.parsers.opexpressionparser.ANY.get_name')
    def test_simplify_operator(self, get_name_mock):
        """Test the simplify operator functionality:
        If a bool AND or OR contain only 1 operator, than it will optimizes the parser and leave it out.
        """
        get_name_mock.return_value = '__ANY_test'
        oparator_json = {"__OR_": [{"__AND_": {"__OR_": [{"__AND_": {"__ANY_prototype": {"__FilterCONST_": True}}}]}}]}
        op_parser = OpExpressionParser()
        self.assertEqual("ANY[test]( const(True) )",
                         str(op_parser.parse(oparator_json)).replace(" ", "").replace("\n", " "))





if __name__ == '__main__':
    unittest.main()
