from abc import ABC, abstractmethod 

class AbstractBoolOperator(ABC):
    """

    """

    @staticmethod
    def prefix_meta_info_paths(op_name, op_result_meta_info):
        """

        :param op_name:
        :param op_result_meta_info:
        :return:
        """
        return [(op_name + ":" + op_path, matching_tag_bundles)
                for (op_path, matching_tag_bundles) in op_result_meta_info]
    
    def get_name(self, elemname, name):
        """

        :param elemname:
        :param name:
        :return:
        """
        return elemname + str(hash(self.filter_operator)) if name in (None, '') or not name.strip() else name

    @staticmethod
    def is_bool_op(op):
        """

        :param op:
        :return:
        """
        return issubclass(type(op), AbstractBoolOperator)

    @staticmethod
    def is_bool_op_list(l):
        """

        :param l:
        :return:
        """
        for op in l:
            if AbstractBoolOperator.is_bool_op(op):
                return True
        return False
  
    @abstractmethod
    def apply(self, tag_bundle_set):
        """

        :param tag_bundle_set:
        :return:
        """
        return True