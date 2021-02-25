import unittest
from openlostcat.category import Category
from openlostcat.categorycatalog import CategoryCatalog
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator
from openlostcat.operators.bool_operators import BoolREF, BoolConst
from openlostcat.operators.filter_operators import FilterREF, FilterConst
from openlostcat.parsers.opexpressionparser import OpExpressionParser
from openlostcat.parsers.categoryorrefdefparser import CategoryOrRefDefParser
from openlostcat.parsers.categorycatalogparser import CategoryCatalogParser
from openlostcat.parsers.refdict import RefDict

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
        oparator_json = {"__OR_": [{"__AND_": {"__OR_": [{"__AND_": {"__ANY_test": {"__FILTERCONST_": True}}}]}}]}
        op_parser = OpExpressionParser()
        self.assertEqual("ANY[test](const(True))",
                         TestParserProcess.__uniform_output(str(op_parser.parse(oparator_json))))

    def test_parser_error(self):
        """Test if exception is raised
        """
        op_parser = OpExpressionParser()
        wrong_jsons = [{"__OR_": {"__FILTERCONST_": True}},
                       {"__AND_": [{"__FILTERCONST_": True}]},
                       {"__NOT_": "#wrong"},
                       {"__REF_": {"__FILTERCONST_": True}},
                       {"__IMPL_": {"__FILTERCONST_": True}},
                       {"__IMPL_": [{"__FILTERCONST_": True}]},
                       {"__IMPL_": [{"__BOOLCONST_": True}]},
                       {"__BOOLCONST_": "#wrong"},
                       {"__FILTERCONST_": "#wrong"},
                       {"key": {"__FILTERCONST_": True}},
                       "wrong",
                       {"__ANY_": {"__BOOLCONST_": True}},
                       {"__ALL_": {"__BOOLCONST_": True}}]
        for wrong_json in wrong_jsons:
            with self.subTest(wrong_json=wrong_json):
                with self.assertRaises(SyntaxError):
                    op_parser.parse(wrong_json)

    def test_operator_equal_creation(self):
        """Test if some operator can be created multiple ways
        """
        op_parser = OpExpressionParser(RefDict({"#test": FilterREF("#test", FilterConst(True))},
                                               {"##test": BoolREF("#test", BoolConst(True))}))
        same_operators = [
            ({"__AND_": {"__FILTERCONST_": True, "__FILTERCONST_": True}},
             {"__FILTERCONST_": True, "__FILTERCONST_": True}),
            ({"__OR_": [{"__FILTERCONST_": True}, {"__FILTERCONST_": True}]},
             [{"__FILTERCONST_": True}, {"__FILTERCONST_": True}]),
            ({"__BOOLCONST_": True}, True),
            ({"__REF_": "#test"}, "#test"),
            ({"__REF_": "##test"}, "##test")
        ]
        for same_operator in same_operators:
            with self.subTest(same_operator=same_operator):
                self.assertEqual(type(op_parser.parse(same_operator[0])), type(op_parser.parse(same_operator[1])))

    def test_operator_filter_bool_variation(self):
        """Test if parser creates the appropriate operator in filter or bool version
        """
        op_parser = OpExpressionParser(RefDict({"#test": FilterREF("#test", FilterConst(True))},
                                               {"##test": BoolREF("#test", BoolConst(True))}))
        bool_filter_operator_pairs = [
            ({"__BOOLCONST_": True, "__BOOLCONST_": True}, {"__FILTERCONST_": True, "__FILTERCONST_": True}),
            ([True, True], [{"__FILTERCONST_": True}, {"__FILTERCONST_": True}]),
            ({"__NOT_": [True]}, {"__NOT_": {"__FILTERCONST_": True}}),
            ("##test", "#test"),
            ({"__IMPL_": [True, True]},
             {"__IMPL_": [{"__FILTERCONST_": True}, {"__FILTERCONST_": True}]})
        ]
        for bool_filter_operator_pair in bool_filter_operator_pairs:
            with self.subTest(bool_filter_operator_pair=bool_filter_operator_pair):
                self.assertTrue(AbstractBoolOperator.is_bool_op(op_parser.parse(bool_filter_operator_pair[0])))
                self.assertFalse(AbstractBoolOperator.is_bool_op(op_parser.parse(bool_filter_operator_pair[1])))

    @patch('openlostcat.parsers.opexpressionparser.ANY.get_name')
    @patch('openlostcat.parsers.opexpressionparser.ALL.get_name')
    def test_category_wrapper_quantifier(self, get_name_mock_any, get_name_mock_all):
        """Test
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
        """Test
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
                         TestParserProcess.__uniform_output(str(ref)))

    @patch('openlostcat.parsers.opexpressionparser.ANY.get_name')
    @patch('openlostcat.parsers.opexpressionparser.ALL.get_name')
    def test_category_cat_parser(self, get_name_mock_any, get_name_mock_all):
        """Test
        """
        get_name_mock_any.return_value = '__ANY_test'
        get_name_mock_all.return_value = '__ALL_test'
        cat_cat_json = {
            "type": "CategoryRuleCollection",
            "properties": {
                "evaluationStrategy": "all"
            },
            "categoryRules": [
                {
                    "water_nearby": {"waterway": "river"}
                },
                {
                    "calm_streets": {
                        "__ALL_not_road": {
                            "__NOT_road": {"highway": ["primary", "secondary"]}
                        }
                    }
                }
            ]
        }
        cat_cat_validation_output = ""

        cat_cat_parser = CategoryCatalogParser()
        cat_cat = cat_cat_parser.parse(cat_cat_json)
        self.assertTrue(isinstance(cat_cat, CategoryCatalog))
        self.assertEqual(cat_cat.evaluationStrategy, "all")
        self.assertEqual(len(cat_cat.categories), 2)
        self.assertEqual(TestParserProcess.__uniform_output(cat_cat_validation_output),
                         # TestParserProcess.__uniform_output(str(cat_cat)))
                         str(cat_cat))


if __name__ == '__main__':
    unittest.main()
