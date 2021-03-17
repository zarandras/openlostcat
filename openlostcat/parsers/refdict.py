from openlostcat.operators.bool_operators import BoolREF
from openlostcat.operators.filter_operators import FilterREF
from openlostcat.utils import error
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator
from openlostcat.operators.abstract_filter_operator import AbstractFilterOperator


class RefDict:
    """Reference dictionary of named subexpressions for (re)using them in category rule expressions

    """

    def __init__(self, filter_ref_dict=None, bool_ref_dict=None):
        """Initializer

        :param filter_ref_dict: An existing set/filter-level ref_dict to be used (optional)
        :param bool_ref_dict:   An existing bool/category-level ref_dict to be used (optional)
        """
        if bool_ref_dict is None:
            bool_ref_dict = {}
        if filter_ref_dict is None:
            filter_ref_dict = {}
        self.bool_ref_dict = bool_ref_dict
        self.filter_ref_dict = filter_ref_dict

    @staticmethod
    def is_ref(ref_name):
        """Utility function determining whether a string is a named subexpression reference

        :param ref_name: input string (name)
        :return: bool
        """
        return ref_name.startswith("#")

    @staticmethod
    def is_bool_ref(ref_name):
        """Utility function determining whether a string is a category/bool-level named subexpression reference

        :param ref_name: input string (name)
        :return: bool
        """
        return ref_name.startswith("##")

    def get_ref(self, ref_name):
        """Retrieves a reference from the dictionary by its name

        :param ref_name: reference name, must start with # for set/filter-level and ## for bool/category-level operators
        :return: the operator (subexpression) stored for the name
        """
        try:
            if self.is_bool_ref(ref_name):
                return self.bool_ref_dict[ref_name]
            elif self.is_ref(ref_name):
                return self.filter_ref_dict[ref_name]
            else:
                error("Syntax error: invalid reference name. A reference name must start with '#': ", ref_name)
        except KeyError:
            error("The given reference can not be found: ", ref_name)

    @staticmethod
    def create_ref(ref_name, operator):
        """Creates a reference operator object
            wraps any set/filter-level operator into a category/bool-level subexpression by a quantifier
            if the reference type is of category/bool level (starts with ##)

        :param ref_name: reference name, must start with # for set/filter-level and ## for bool/category-level operators
        :param operator: subexpression to be named and stored
        :return: reference operator object to be stored in a ref.dict and to be used as a subexpression
        """
        if not RefDict.is_ref(ref_name):
            error("Syntax error: invalid reference name. A reference name must start with '#': ", ref_name)
        if RefDict.is_bool_ref(ref_name):
            return BoolREF(ref_name, AbstractFilterOperator.get_as_bool_op(operator))
        else:
            if AbstractBoolOperator.is_bool_op(operator):
                error("Invalid reference definition. A bool expression is given but a filter expression is expected: ",
                      operator)
            return FilterREF(ref_name, operator)

    def set_ref(self, ref_operator):
        """Stores a reference operator (named subexpression) in the dictionary

        :param ref_operator: a bool/filter ref operator to be stored
        """
        switcher = {
            BoolREF: self.bool_ref_dict,
            FilterREF: self.filter_ref_dict
        }
        ref_dict = switcher.get(type(ref_operator), lambda x: error("Invalid reference operator: ", x))
        if ref_operator.name in ref_dict:
            error("Reference already exists. Duplicate reference definition: ", ref_operator.name)
        ref_dict[ref_operator.name] = ref_operator
