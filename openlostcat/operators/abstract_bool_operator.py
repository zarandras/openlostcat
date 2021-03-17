from abc import ABC, abstractmethod 


class AbstractBoolOperator(ABC):
    """Ancestor class for the category-level (bool) operators
    """

    @staticmethod
    def prefix_meta_info_paths(op_name, op_result_meta_info):
        """Retrieves the results of the subexpressions under this operator (for debug)

        :param op_name:
        :param op_result_meta_info:
        :return:
        """
        return [(op_name + ":" + op_path, matching_tag_bundles)
                for (op_path, matching_tag_bundles) in op_result_meta_info]

    @staticmethod
    def get_name(unit_name, name, unique_member_variable):
        """Generates a unique name if no operator name is given (used for quantifiers only)

        :param unique_member_variable:
        :param unit_name:
        :param name:
        :return:
        """
        return unit_name + str(hash(unique_member_variable)) if name in (None, '') or not name.strip() else name

    @staticmethod
    def is_bool_op(op):
        """Utility function determining whether an operator is of bool level

        :param op: operator
        :return:   boolean - True: is bool op
        """
        return issubclass(type(op), AbstractBoolOperator)

    @staticmethod
    def is_bool_op_list(op_list):
        """Utility function determining whether an operator list is of bool level (at least one of them)

        :param op_list: operator list
        :return:        boolean - True: is bool op list
        """
        for op in op_list:
            if AbstractBoolOperator.is_bool_op(op):
                return True
        return False
  
    @abstractmethod
    def apply(self, tag_bundle_set):
        """Evaluates the operator (subexpression) for the given tag bundle set

        :param tag_bundle_set: tag bundle set of the osm objects at/near the location
        :return: boolean result of the operator (subexpression)
        """
        return True
