from docutils import nodes
from docutils.statemachine import ViewList
from nose.util import resolve_name


def docstring_directive(dirname, arguments, options, content, lineno,
                        content_offset, block_text, state, state_machine):
    obj_name = arguments[0]
    obj = resolve_name(obj_name)
    rst = ViewList()
    rst.append(obj.__doc__, '<docstring>')
    print "CALLED", obj_name, obj, rst
    node = nodes.section()
    surrounding_title_styles = state.memo.title_styles
    surrounding_section_level = state.memo.section_level
    state.memo.title_styles = []
    state.memo.section_level = 0
    state.nested_parse(rst, 0, node, match_titles=1)
    state.memo.title_styles = surrounding_title_styles
    state.memo.section_level = surrounding_section_level
    return node.children


def setup(app):
    app.add_directive('docstring', docstring_directive, 1, (1, 0, 1))
