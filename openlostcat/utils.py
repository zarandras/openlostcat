import textwrap

base_indent_num = 4

def indent(text, amount, ch=' '):
    return textwrap.indent(text, amount * ch)


def error(text, t):
    raise SyntaxError(text + str(t))
