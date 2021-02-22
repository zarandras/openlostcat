import unittest
from openlostcat.operators.filter_operators import FilterConst, FilterREF
from openlostcat.operators.bool_operators import BoolConst, BoolREF
from openlostcat.parsers.refdict import RefDict

from openlostcat.parsers.opexpressionparser import OpExpressionParser
from openlostcat.parsers.categoryorrefdefparser import CategoryOrRefDefParser
from openlostcat.parsers.categorycatalogparser import CategoryOrRefDefParser

from unittest.mock import MagicMock


class TestParserProcess(unittest.TestCase):

    def test_simplify_operator(self):
        """Test the simplify operator functionality:
        If a bool AND or OR contain only 1 operator, than it will optimizes the parser and leave it out.
        """
        oparator_json = {"__OR_": [{"__AND_": {"__ANY_": {"__FilterCONST_": True}}}]}
        op_parser = OpExpressionParser()
        self.assertEqual(str(op_parser.parse(oparator_json)).replace(" ", "").replace("\n", " "), "test")


if __name__ == '__main__':
    unittest.main()
