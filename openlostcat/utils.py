"""
Utils what for
"""

import textwrap
from immutabledict import immutabledict

base_indent_num = 4
""" Base_indent_num... """

def indent(text, amount, ch=' '):
    """

    :param text:
    :param amount:
    :param ch:
    :return:
    """
    return textwrap.indent(text, amount * ch)


def error(text, t):
    """

    :param text:
    :param t:
    :return:
    """
    raise SyntaxError(text + str(t))

def to_tag_bundle(tag_dict):
    """

    :param tag_dict:
    :return:
    """
    return immutabledict(tag_dict)

def to_tag_bundle_set(tag_dict_list):
    """

    :param tag_dict_list:
    :return:
    """
    return {to_tag_bundle(tag_dict) for tag_dict in tag_dict_list}

def get_tags_from_osm_elements(osm_json_dict):
    """

    :param osm_json_dict:
    :return:
    """
    return [elements['tags'] for elements in osm_json_dict['elements'] if 'tags' in elements]

