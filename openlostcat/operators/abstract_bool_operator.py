from abc import ABC, abstractmethod 

class AbstractBoolOperator(ABC):

    @staticmethod
    def prefix_meta_info_paths(op_name, op_result_meta_info):
        return [(op_name + ":" + op_path, matching_tag_bundles)
                for (op_path, matching_tag_bundles) in op_result_meta_info]
    
    def get_name(self, elemname, name):
        return elemname + str(hash(self.filter_operator)) if name in (None, '') or not name.strip() else name
  
    @abstractmethod
    def apply(self, tags): 
        return True