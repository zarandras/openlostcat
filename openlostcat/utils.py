import textwrap
from immutabledict import immutabledict

base_indent_num = 4

def indent(text, amount, ch=' '):
    return textwrap.indent(text, amount * ch)


def error(text, t):
    raise SyntaxError(text + str(t))

def to_tag_bundle(tag_dict):
    return immutabledict(tag_dict)

# def list of dict to_tag_bundle_set(list<dict>)
def to_tag_bundle_set(tag_dict_list):
    return {to_tag_bundle(tag_dict) for tag_dict in tag_dict_list}

def get_tags_from_osm_elements(osm_json_dict):
    return [elements['tags'] for elements in osm_json_dict['elements'] if 'tags' in elements]

