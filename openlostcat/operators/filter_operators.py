from .abstract_filter_operator import AbstractFilterOperator
from openlostcat.utils import error, indent, base_indent_num
from openlostcat.operators.quantifier_operators import ANY, ALL


class FilterAND(AbstractFilterOperator):
    """Set (filter)-level 'and' operator (subexpression with tag bundle set operands)

    """

    str_template = "and(\n{operators}\n)"

    @staticmethod
    def __choose_wrapper_quantifier(filter_operators):
        """wrapper quantifier of 'and' will default to ALL if each subexpression defaults to ALL,
        otherwise it will default to ANY

        :param filter_operators: operands
        :return: default wrapper quantifier ALL/ANY
        """
        return ALL if all([issubclass(op.wrapper_quantifier, ALL) for op in filter_operators]) else ANY

    def __init__(self, filter_operators):
        self.filter_operators = filter_operators
        self.wrapper_quantifier = self.__choose_wrapper_quantifier(filter_operators)

    def apply(self, tag_bundle_set):
        matching_tag_bundles = tag_bundle_set
        for op in self.filter_operators:
            matching_tag_bundles = op.apply(matching_tag_bundles)
            if len(matching_tag_bundles) <= 0:
                return matching_tag_bundles
        return matching_tag_bundles

    def __str__(self):
        return self.str_template.format(operators=indent(
            '\n'.join([str(operator) for operator in self.filter_operators]),
            base_indent_num))


class FilterOR(AbstractFilterOperator):
    """Set (filter)-level 'or' operator (subexpression with tag bundle set operands)

    """

    str_template = "or[\n{operators}\n]"

    @staticmethod
    def __choose_wrapper_quantifier(filter_operators):
        """wrapper quantifier of 'or' will default to ALL if at least one subexpression defaults to ALL,
        otherwise it will default to ANY

        :param filter_operators: operands
        :return: default wrapper quantifier ALL/ANY
        """
        return ALL if any([issubclass(op.wrapper_quantifier, ALL) for op in filter_operators]) else ANY

    def __init__(self, filter_operators):
        self.filter_operators = filter_operators
        self.wrapper_quantifier = self.__choose_wrapper_quantifier(filter_operators)

    def apply(self, tag_bundle_set):
        result = set()
        candidates = tag_bundle_set
        for op in self.filter_operators:
            matching_tag_bundles = op.apply(candidates)
            candidates = candidates - matching_tag_bundles
            result.update(matching_tag_bundles)
            if len(result) == len(tag_bundle_set):
                return result
        return result

    def __str__(self):
        return self.str_template.format(operators=indent(
            '\n'.join([str(operator) for operator in self.filter_operators]),
            base_indent_num))


class FilterNOT(AbstractFilterOperator):
    """Set (filter)-level 'not' operator (subexpression with a tag bundle set operand)

    """

    str_template = "not(\n{operator}\n)"

    def __init__(self, filter_operator):
        self.filter_operator = filter_operator

        # wrapper quantifier is inherited from its subexpression
        self.wrapper_quantifier = filter_operator.wrapper_quantifier

    def apply(self, tag_bundle_set):
        return tag_bundle_set - self.filter_operator.apply(tag_bundle_set)

    def __str__(self):
        return self.str_template.format(operator=indent(str(self.filter_operator), base_indent_num))


class FilterREF(AbstractFilterOperator):
    """Set (filter)-level reference subexpression (tag bundle set type)

    """

    str_template = "ref {name}(\n{operator}\n)"

    def __init__(self, name, filter_operator):
        self.name = name
        self.filter_operator = filter_operator

        # wrapper quantifier is inherited from its subexpression
        self.wrapper_quantifier = filter_operator.wrapper_quantifier

    def apply(self, tag_bundle_set):
        return self.filter_operator.apply(tag_bundle_set)

    def __str__(self):
        return self.str_template.format(name=self.name, operator=indent(str(self.filter_operator), base_indent_num))


class FilterIMPL(AbstractFilterOperator):
    """Set (filter)-level implication operator (subexpression with tag bundle set operands)

    """

    str_template = "impl(\n{operators}\n)"

    def __init__(self, filter_operators):
        if len(filter_operators) < 2:
            error("Implication must contain at least 2 elements: ", filter_operators)
        self.filter_operators = filter_operators
        self.impl_op = FilterOR([FilterNOT(op) for op in filter_operators[:-1]] + [filter_operators[-1]])

        # wrapper quantifier of implication will default to ALL
        self.wrapper_quantifier = ALL

    def apply(self, tag_bundle_set):
        return self.impl_op.apply(tag_bundle_set)

    def __str__(self):
        return self.str_template.format(operators=indent(
            '\n => \n'.join([str(operator) for operator in self.filter_operators]),
            base_indent_num))


class AtomicFilter(AbstractFilterOperator):
    """Tag-based atomic filter operator
    Accepting a key - value pair or a key - value list for matching with the tag bundle set given
    """

    str_template = "{{{key} : {value}}}, is_optional_key = {is_optional_key}"

    @staticmethod
    def __parse_single_value(dat):
        """Gets a single value from dat

        :param dat: value as string, bool or int (or None as null)
        :return: value in string
        """
        switcher = {
            bool: lambda b: "yes" if b else "no",
            int: lambda i: str(i),
            str: lambda s: s,
            type(None): lambda x: None,
            list: lambda x: error("Array is not allowed here: ", x),
            dict: lambda x: error("Key-value dictionary is not allowed here: ", x)
        }
        return switcher.get(type(dat),
                            lambda x: error("Unexpected element. Value type is not allowed here: ", x))(dat)

    @staticmethod
    def __parse_values(value):
        if isinstance(value, list):
            return {AtomicFilter.__parse_single_value(e) for e in value}
        else:
            return {AtomicFilter.__parse_single_value(value)}

    def __init__(self, key, value):
        """Initializer
        :param key: tag name string
        :param value: tag value (various types allowed) or a value list
        """
        self.key = key
        self.values = AtomicFilter.__parse_values(value)
        self.is_optional_key = None in self.values
        if self.is_optional_key:
            self.values = set(filter(None, self.values))

        # wrapper quantifier of an atomic filter will default to ANY
        self.wrapper_quantifier = ANY

    def __check_condition(self, tag_bundle):
        return (self.is_optional_key and self.key not in tag_bundle) or (
                self.key in tag_bundle and tag_bundle[self.key] in self.values)

    def apply(self, tag_bundle_set):
        return {tag_bundle for tag_bundle in tag_bundle_set if self.__check_condition(tag_bundle)}

    def __str__(self):
        return self.str_template.format(key=self.key, value=self.values, is_optional_key=self.is_optional_key)


class FilterConst(AbstractFilterOperator):
    """Set (filter)-level constant subexpression (tag bundle set type)
    A filter constant True returns the operand, False returns the empty set
    """

    str_template = "const({const})"

    def __init__(self, const_val):
        """Initializer

        :param const_val: True/False
        """
        if not isinstance(const_val, bool):
            error("FilterConst must be initialized with a bool value.", const_val)
        self.const_val = const_val

        # wrapper quantifier of a const filter will default to ANY
        self.wrapper_quantifier = ANY

    def apply(self, tag_bundle_set):
        return tag_bundle_set if self.const_val else set()

    def __str__(self):
        return self.str_template.format(const=self.const_val)
