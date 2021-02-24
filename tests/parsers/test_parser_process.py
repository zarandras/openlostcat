import unittest
from openlostcat.category import Category
from openlostcat.operators.bool_operators import BoolREF
from openlostcat.parsers.opexpressionparser import OpExpressionParser
from openlostcat.parsers.categoryorrefdefparser import CategoryOrRefDefParser
from openlostcat.parsers.categorycatalogparser import CategoryCatalogParser

from unittest.mock import patch
from unittest.mock import MagicMock


class TestParserProcess(unittest.TestCase):

    @staticmethod
    def __uniform_output(out):
        return out.replace(" ", "").replace("\n", "")

    def test_simplify_operator(self):
        """Test the simplify operator functionality:
        If a bool AND or OR contain only 1 operator, than it will optimizes the parser and leave it out.
        """
        oparator_json = {"__OR_": [{"__AND_": {"__OR_": [{"__AND_": {"__ANY_test": {"__FilterCONST_": True}}}]}}]}
        op_parser = OpExpressionParser()
        self.assertEqual("ANY[test]( const(True) )",
                         TestParserProcess.__uniform_output(str(op_parser.parse(oparator_json))))

    @patch('openlostcat.parsers.opexpressionparser.ANY.get_name')
    @patch('openlostcat.parsers.opexpressionparser.ALL.get_name')
    def test_category_wrapper_quantifier(self, get_name_mock_any, get_name_mock_all):
        """Test the simplify operator functionality:
        If a bool AND or OR contain only 1 operator, than it will optimizes the parser and leave it out.
        """
        get_name_mock_any.return_value = '__ANY_test'
        get_name_mock_all.return_value = '__ALL_test'
        category_json = {
            "test_category": [
                {
                    "__IMPL_1": [
                        {"landuse": "residential"}, {"landuse": "residential"}, {"landuse": "residential"}
                    ],
                    "__IMPL_2": [
                        {"landuse": "residential"}, {"landuse": "residential"}, {"landuse": "residential"}
                    ],
                    "landuse": "residential"

                },
                {"landuse": "residential"},
                {"__IMPL_1": [
                    {"landuse": "residential"}, {"landuse": "residential"}, {"landuse": "residential"}
                ]}
            ]
        }
        category_validation_output = "Category name: test_category \
                                    rules: [ \
                                        OR[ \
                                            ANY[test]( \
                                                and( \
                                                    impl( \
                                                            {landuse : {'residential'}}, is_optional_key = False \
                                                            => \
                                                            {landuse : {'residential'}}, is_optional_key = False \
                                                            => \
                                                            {landuse : {'residential'}}, is_optional_key = False \
                                                        ) \
                                                    impl( \
                                                            {landuse : {'residential'}}, is_optional_key = False \
                                                            => \
                                                            {landuse : {'residential'}}, is_optional_key = False \
                                                            => \
                                                            {landuse : {'residential'}}, is_optional_key = False \
                                                        ) \
                                                            {landuse : {'residential'}}, is_optional_key = False \
                                                ) \
                                            ) \
                                            ANY[test]( \
                                                {landuse : {'residential'}}, is_optional_key = False \
                                            ) \
                                            ALL[test]( \
                                                impl( \
                                                    {landuse : {'residential'}}, is_optional_key = False \
                                                    => \
                                                    {landuse : {'residential'}}, is_optional_key = False \
                                                    => \
                                                    {landuse : {'residential'}}, is_optional_key = False \
                                                ) \
                                            ) \
                                        ] \
                                    ]"

        category_ref_parser = CategoryOrRefDefParser()
        category = category_ref_parser.parse(category_json)
        self.assertTrue(isinstance(category, Category))
        self.assertEqual(TestParserProcess.__uniform_output(category_validation_output),
                         TestParserProcess.__uniform_output(str(category)))

    @patch('openlostcat.parsers.opexpressionparser.ANY.get_name')
    @patch('openlostcat.parsers.opexpressionparser.ALL.get_name')
    def test_ref_parser(self, get_name_mock_any, get_name_mock_all):
        """Test the simplify operator functionality:
        If a bool AND or OR contain only 1 operator, than it will optimizes the parser and leave it out.
        """
        get_name_mock_any.return_value = '__ANY_test'
        get_name_mock_all.return_value = '__ALL_test'
        ref_json = {
            "##test_ref": [
                {
                    "__IMPL_1": [
                        {"landuse": "residential"}, {"landuse": "residential"}, {"landuse": "residential"}
                    ],
                    "__IMPL_2": [
                        {"landuse": "residential"}, {"landuse": "residential"}, {"landuse": "residential"}
                    ],
                    "landuse": "residential"

                },
                {"landuse": "residential"},
                {"__IMPL_1": [
                    {"landuse": "residential"}, {"landuse": "residential"}, {"landuse": "residential"}
                ]}
            ]
        }
        ref_validation_output = "REF ##test_ref( \
                    ALL[test]( \
                            or[ \
                                and( \
                                    impl( \
                                        {landuse : {'residential'}}, is_optional_key = False \
                                        => \
                                        {landuse : {'residential'}}, is_optional_key = False \
                                        => \
                                        {landuse : {'residential'}}, is_optional_key = False \
                                    ) \
                                impl( \
                                    {landuse : {'residential'}}, is_optional_key = False \
                                    => \
                                    {landuse : {'residential'}}, is_optional_key = False \
                                    => \
                                    {landuse : {'residential'}}, is_optional_key = False \
                                ) \
                                {landuse : {'residential'}}, is_optional_key = False \
                                ) \
                                {landuse : {'residential'}}, is_optional_key = False \
                                impl( \
                                    {landuse : {'residential'}}, is_optional_key = False \
                                => \
                                {landuse : {'residential'}}, is_optional_key = False \
                                => \
                                {landuse : {'residential'}}, is_optional_key = False \
                                ) \
                            ] \
                    ) \
            )"

        category_ref_parser = CategoryOrRefDefParser()
        ref = category_ref_parser.parse(ref_json)
        self.assertTrue(isinstance(ref, BoolREF))
        self.assertEqual(TestParserProcess.__uniform_output(ref_validation_output),
                         str(ref))
        # TestParserProcess.__uniform_output(str(ref))


if __name__ == '__main__':
    unittest.main()
