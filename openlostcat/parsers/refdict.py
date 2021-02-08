from openlostcat.operators.bool_operators import BoolREF
from openlostcat.operators.filter_operators import FilterREF
from openlostcat.utils import error
from openlostcat.operators.abstract_bool_operator import AbstractBoolOperator
from openlostcat.operators.abstract_filter_operator import AbstractFilterOperator


class RefDict:
    """

    """

    def __init__(self, filter_ref_dict = {}, bool_ref_dict = {}):
        """

        :param filter_ref_dict:
        :param bool_ref_dict:
        """
        self.bool_ref_dict = bool_ref_dict
        self.filter_ref_dict = filter_ref_dict

    @staticmethod
    def is_ref(ref_name):
        """

        :param ref_name:
        :return:
        """
        return ref_name.startswith("#")

    @staticmethod
    def is_bool_ref(ref_name):
        """

        :param ref_name:
        :return:
        """
        return ref_name.startswith("##")

    def get_ref(self, ref_name):
        """

        :param ref_name:
        :return:
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
        """

        :param ref_name:
        :param operator:
        :return:
        """
        if not RefDict.is_ref(ref_name):
            error("Syntax error: invalid reference name. A reference name must start with '#': ", ref_name)
        if RefDict.is_bool_ref(ref_name):
            return BoolREF(ref_name, AbstractFilterOperator.get_as_bool_op(operator))
        else:
            if AbstractBoolOperator.is_bool_op(operator):
                error("Invalid reference definition. A bool expression is given but a filter expression is expected: ", operator)
            return FilterREF(ref_name, operator)

    def set_ref(self, ref_operator):
        """

        :param ref_operator:
        :return:
        """
        switcher = {
            BoolREF:   self.bool_ref_dict,
            FilterREF: self.filter_ref_dict
        }
        switcher.get(type(ref_operator),
                     lambda x: error("Invalid reference operator: ", x))(ref_operator)[ref_operator.name] = ref_operator


    # def set_ref(self, ref_operator):
    #     """
    #
    #     :param ref_operator:
    #     :return:
    #     """
    #     switcher = {
    #         openlostcat.operators.bool_operators.BoolREF:     lambda ref: self.bool_ref_dict[ref.name]   = ref,
    #         openlostcat.operators.filter_operators.FilterREF: lambda ref: self.filter_ref_dict[ref.name] = ref
    #     }
    #     switcher.get(type(ref_operator),
    #                  lambda x: error("Invalid reference operator: ", x))(ref_operator)

