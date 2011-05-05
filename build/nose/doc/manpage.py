# $Id: manpage.py 5901 2009-04-07 13:26:48Z grubert $
# Author: Engelbert Gruber <grubert@users.sourceforge.net>
# Copyright: This module is put into the public domain.

"""
Simple man page writer for reStructuredText.

Man pages (short for "manual pages") contain system documentation on unix-like
systems. The pages are grouped in numbered sections: 

 1 executable programs and shell commands
 2 system calls
 3 library functions
 4 special files
 5 file formats
 6 games
 7 miscellaneous
 8 system administration

Man pages are written *troff*, a text file formatting system.

See http://www.tldp.org/HOWTO/Man-Page for a start.

Man pages have no subsection only parts.
Standard parts

  NAME ,
  SYNOPSIS ,
  DESCRIPTION ,
  OPTIONS ,
  FILES ,
  SEE ALSO ,
  BUGS ,

and

  AUTHOR .

A unix-like system keeps an index of the DESCRIPTIONs, which is accesable
by the command whatis or apropos.

"""

# NOTE: the macros only work when at line start, so try the rule
#       start new lines in visit_ functions.

__docformat__ = 'reStructuredText'

import sys
import os
import time
import re
from types import ListType

import docutils
from docutils import nodes, utils, writers, languages

FIELD_LIST_INDENT = 7
DEFINITION_LIST_INDENT = 7
OPTION_LIST_INDENT = 7
BLOCKQOUTE_INDENT = 3.5

# Define two macros so man/roff can calculate the
# indent/unindent margins by itself
MACRO_DEF = (r"""
.nr rst2man-indent-level 0
.
.de1 rstReportMargin
\\$1 \\n[an-margin]
level \\n[rst2man-indent-level]
level magin: \\n[rst2man-indent\\n[rst2man-indent-level]]
-
\\n[rst2man-indent0]
\\n[rst2man-indent1]
\\n[rst2man-indent2]
..
.de1 INDENT
.\" .rstReportMargin pre:
. RS \\$1
. nr rst2man-indent\\n[rst2man-indent-level] \\n[an-margin]
. nr rst2man-indent-level +1
.\" .rstReportMargin post:
..
.de UNINDENT
. RE
.\" indent \\n[an-margin]
.\" old: \\n[rst2man-indent\\n[rst2man-indent-level]]
.nr rst2man-indent-level -1
.\" new: \\n[rst2man-indent\\n[rst2man-indent-level]]
.in \\n[rst2man-indent\\n[rst2man-indent-level]]u
..
""")

class Writer(writers.Writer):

    supported = ('manpage')
    """Formats this writer supports."""

    output = None
    """Final translated form of `document`."""

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = Translator

    def translate(self):
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()


class Table:
    def __init__(self):
        self._rows = []
        self._options = ['center', ]
        self._tab_char = '\t'
        self._coldefs = []
    def new_row(self):
        self._rows.append([])
    def append_cell(self, cell_lines):
        """cell_lines is an array of lines"""
        self._rows[-1].append(cell_lines)
        if len(self._coldefs) < len(self._rows[-1]):
            self._coldefs.append('l')
    def astext(self):
        text = '.TS\n'
        text += ' '.join(self._options) + ';\n'
        text += '|%s|.\n' % ('|'.join(self._coldefs))
        for row in self._rows:
            # row = array of cells. cell = array of lines.
            # line above 
            text += '_\n'
            max_lns_in_cell = 0
            for cell in row:
                max_lns_in_cell = max(len(cell), max_lns_in_cell)
            for ln_cnt in range(max_lns_in_cell):
                line = []
                for cell in row:
                    if len(cell) > ln_cnt:
                        line.append(cell[ln_cnt])
                    else:
                        line.append(" ")
                text += self._tab_char.join(line) + '\n'
        text += '_\n'
        text += '.TE\n'
        return text

class Translator(nodes.NodeVisitor):
    """"""

    words_and_spaces = re.compile(r'\S+| +|\n')
    document_start = """Man page generated from reStructeredText."""

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = settings = document.settings
        lcode = settings.language_code
        self.language = languages.get_language(lcode)
        self.head = []
        self.body = []
        self.foot = []
        self.section_level = -1
        self.context = []
        self.topic_class = ''
        self.colspecs = []
        self.compact_p = 1
        self.compact_simple = None
        # the list style "*" bullet or "#" numbered
        self._list_char = []
        # writing the header .TH and .SH NAME is postboned after
        # docinfo.
        self._docinfo = {
                "title" : "", "subtitle" : "",
                "manual_section" : "", "manual_group" : "",
                "author" : "", 
                "date" : "", 
                "copyright" : "",
                "version" : "",
                    }
        self._in_docinfo = 1 # FIXME docinfo not being found?
        self._active_table = None
        self._in_entry = None
        self.header_written = 0
        self.authors = []
        self.section_level = -1
        self._indent = [0]
        # central definition of simple processing rules
        # what to output on : visit, depart
        self.defs = {
                'indent' : ('.INDENT %.1f\n', '.UNINDENT\n'),
                'definition' : ('', ''),
                'definition_list' : ('', '.TP 0\n'),
                'definition_list_item' : ('\n.TP', ''),
                #field_list
                #field
                'field_name' : ('\n.TP\n.B ', '\n'),
                'field_body' : ('', '.RE\n', ),
                'literal' : ('\\fB', '\\fP'),
                'literal_block' : ('\n.nf\n', '\n.fi\n'),

                #option_list
                'option_list_item' : ('\n.TP', ''),
                #option_group, option
                'description' : ('\n', ''),
                
                'reference' : (r'\fI\%', r'\fP'),
                #'target'   : (r'\fI\%', r'\fP'),
                'emphasis': ('\\fI', '\\fP'),
                'strong' : ('\\fB', '\\fP'),
                'term' : ('\n.B ', '\n'),
                'title_reference' : ('\\fI', '\\fP'),

                'problematic' : ('\n.nf\n', '\n.fi\n'),
                # docinfo fields.
                'address' : ('\n.nf\n', '\n.fi\n'),
                'organization' : ('\n.nf\n', '\n.fi\n'),
                    }
        # TODO dont specify the newline before a dot-command, but ensure
        # check it is there.

    def comment_begin(self, text):
        """Return commented version of the passed text WITHOUT end of line/comment."""
        prefix = '\n.\\" '
        return prefix+prefix.join(text.split('\n'))

    def comment(self, text):
        """Return commented version of the passed text."""
        return self.comment_begin(text)+'\n'

    def astext(self):
        """Return the final formatted document as a string."""
        if not self.header_written:
            # ensure we get a ".TH" as viewers require it.
            self.head.append(self.header())
        return ''.join(self.head + self.body + self.foot)

    def visit_Text(self, node):
        text = node.astext().replace('-','\-')
        text = text.replace("'","\\'")
        self.body.append(text)

    def depart_Text(self, node):
        pass

    def list_start(self, node):
        class enum_char:
            enum_style = {
                    'arabic'     : (3,1),
                    'loweralpha' : (3,'a'),
                    'upperalpha' : (3,'A'),
                    'lowerroman' : (5,'i'),
                    'upperroman' : (5,'I'),
                    'bullet'     : (2,'\\(bu'),
                    'emdash'     : (2,'\\(em'),
                     }
            def __init__(self, style):
                if style == 'arabic':
                    if node.has_key('start'):
                        start = node['start']
                    else:
                        start = 1
                    self._style = (
                            len(str(len(node.children)))+2,
                            start )
                # BUG: fix start for alpha
                else:
                    self._style = self.enum_style[style]
                self._cnt = -1
            def next(self):
                self._cnt += 1
                # BUG add prefix postfix
                try:
                    return "%d." % (self._style[1] + self._cnt)
                except:
                    if self._style[1][0] == '\\':
                        return self._style[1]
                    # BUG romans dont work
                    # BUG alpha only a...z
                    return "%c." % (ord(self._style[1])+self._cnt)
            def get_width(self):
                return self._style[0]
            def __repr__(self):
                return 'enum_style%r' % list(self._style)

        if node.has_key('enumtype'):
            self._list_char.append(enum_char(node['enumtype']))
        else:
            self._list_char.append(enum_char('bullet'))
        if len(self._list_char) > 1:
            # indent nested lists
            # BUG indentation depends on indentation of parent list.
            self.indent(self._list_char[-2].get_width())
        else:
            self.indent(self._list_char[-1].get_width())

    def list_end(self):
        self.dedent()
        self._list_char.pop()

    def header(self):
        tmpl = (".TH %(title)s %(manual_section)s"
                " \"%(date)s\" \"%(version)s\" \"%(manual_group)s\"\n"
                ".SH NAME\n"
                "%(title)s \- %(subtitle)s\n")
        return tmpl % self._docinfo

    def append_header(self):
        """append header with .TH and .SH NAME"""
        # TODO before everything
        # .TH title section date source manual
        if self.header_written:
            return
        self.body.append(self.header())
        self.body.append(MACRO_DEF)
        self.header_written = 1

    def visit_address(self, node):
        self._docinfo['address'] = node.astext()
        raise nodes.SkipNode

    def depart_address(self, node):
        pass

    def visit_admonition(self, node, name):
        self.visit_block_quote(node)

    def depart_admonition(self):
        self.depart_block_quote(None)

    def visit_attention(self, node):
        self.visit_admonition(node, 'attention')

    def depart_attention(self, node):
        self.depart_admonition()

    def visit_author(self, node):
        self._docinfo['author'] = node.astext()
        raise nodes.SkipNode

    def depart_author(self, node):
        pass

    def visit_authors(self, node):
        self.body.append(self.comment('visit_authors'))

    def depart_authors(self, node):
        self.body.append(self.comment('depart_authors'))

    def visit_block_quote(self, node):
        #self.body.append(self.comment('visit_block_quote'))
        # BUG/HACK: indent alway uses the _last_ indention,
        # thus we need two of them.
        self.indent(BLOCKQOUTE_INDENT)
        self.indent(0)

    def depart_block_quote(self, node):
        #self.body.append(self.comment('depart_block_quote'))
        self.dedent()
        self.dedent()

    def visit_bullet_list(self, node):
        self.list_start(node)

    def depart_bullet_list(self, node):
        self.list_end()

    def visit_caption(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'p', '', CLASS='caption'))

    def depart_caption(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('</p>\n')

    def visit_caution(self, node):
        self.visit_admonition(node, 'caution')

    def depart_caution(self, node):
        self.depart_admonition()

    def visit_citation(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'table', CLASS='citation',
                                       frame="void", rules="none"))
        self.body.append('<colgroup><col class="label" /><col /></colgroup>\n'
                         '<col />\n'
                         '<tbody valign="top">\n'
                         '<tr>')
        self.footnote_backrefs(node)

    def depart_citation(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('</td></tr>\n'
                         '</tbody>\n</table>\n')

    def visit_citation_reference(self, node):
        raise NotImplementedError, node.astext()
        href = ''
        if node.has_key('refid'):
            href = '#' + node['refid']
        elif node.has_key('refname'):
            href = '#' + self.document.nameids[node['refname']]
        self.body.append(self.starttag(node, 'a', '[', href=href,
                                       CLASS='citation-reference'))

    def depart_citation_reference(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(']</a>')

    def visit_classifier(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(' <span class="classifier-delimiter">:</span> ')
        self.body.append(self.starttag(node, 'span', '', CLASS='classifier'))

    def depart_classifier(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('</span>')

    def visit_colspec(self, node):
        self.colspecs.append(node)

    def depart_colspec(self, node):
        pass

    def write_colspecs(self):
        self.body.append("%s.\n" % ('L '*len(self.colspecs)))

    def visit_comment(self, node,
                      sub=re.compile('-(?=-)').sub):
        self.body.append(self.comment(node.astext()))
        raise nodes.SkipNode

    def visit_contact(self, node):
        self.visit_docinfo_item(node, 'contact')

    def depart_contact(self, node):
        self.depart_docinfo_item()

    def visit_copyright(self, node):
        self._docinfo['copyright'] = node.astext()
        raise nodes.SkipNode

    def visit_danger(self, node):
        self.visit_admonition(node, 'danger')

    def depart_danger(self, node):
        self.depart_admonition()

    def visit_date(self, node):
        self._docinfo['date'] = node.astext()
        raise nodes.SkipNode

    def visit_decoration(self, node):
        pass

    def depart_decoration(self, node):
        pass

    def visit_definition(self, node):
        self.body.append(self.defs['definition'][0])

    def depart_definition(self, node):
        self.body.append(self.defs['definition'][1])

    def visit_definition_list(self, node):
        self.indent(DEFINITION_LIST_INDENT)

    def depart_definition_list(self, node):
        self.dedent()

    def visit_definition_list_item(self, node):
        self.body.append(self.defs['definition_list_item'][0])

    def depart_definition_list_item(self, node):
        self.body.append(self.defs['definition_list_item'][1])

    def visit_description(self, node):
        self.body.append(self.defs['description'][0])

    def depart_description(self, node):
        self.body.append(self.defs['description'][1])

    def visit_docinfo(self, node):
        self._in_docinfo = 1

    def depart_docinfo(self, node):
        self._in_docinfo = None
        # TODO nothing should be written before this
        self.append_header()

    def visit_docinfo_item(self, node, name):
        self.body.append(self.comment('%s: ' % self.language.labels[name]))
        if len(node):
            return
            if isinstance(node[0], nodes.Element):
                node[0].set_class('first')
            if isinstance(node[0], nodes.Element):
                node[-1].set_class('last')

    def depart_docinfo_item(self):
        pass

    def visit_doctest_block(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'pre', CLASS='doctest-block'))

    def depart_doctest_block(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('\n</pre>\n')

    def visit_document(self, node):
        self.body.append(self.comment(self.document_start).lstrip())
        # writing header is postboned
        self.header_written = 0

    def depart_document(self, node):
        if self._docinfo['author']:
            self.body.append('\n.SH AUTHOR\n%s\n' 
                    % self._docinfo['author'])
        if 'organization' in self._docinfo:
            self.body.append(self.defs['organization'][0])
            self.body.append(self._docinfo['organization'])
            self.body.append(self.defs['organization'][1])
        if 'address' in self._docinfo:
            self.body.append(self.defs['address'][0])
            self.body.append(self._docinfo['address'])
            self.body.append(self.defs['address'][1])
        if self._docinfo['copyright']:
            self.body.append('\n.SH COPYRIGHT\n%s\n' 
                    % self._docinfo['copyright'])
        self.body.append(
                self.comment(
                        'Generated by docutils manpage writer on %s.\n' 
                        % (time.strftime('%Y-%m-%d %H:%M')) ) )

    def visit_emphasis(self, node):
        self.body.append(self.defs['emphasis'][0])

    def depart_emphasis(self, node):
        self.body.append(self.defs['emphasis'][1])

    def visit_entry(self, node):
        # BUG entries have to be on one line separated by tab force it.
        self.context.append(len(self.body))
        self._in_entry = 1

    def depart_entry(self, node):
        start = self.context.pop()
        self._active_table.append_cell(self.body[start:])
        del self.body[start:]
        self._in_entry = 0

    def visit_enumerated_list(self, node):
        self.list_start(node)

    def depart_enumerated_list(self, node):
        self.list_end()

    def visit_error(self, node):
        self.visit_admonition(node, 'error')

    def depart_error(self, node):
        self.depart_admonition()

    def visit_field(self, node):
        #self.body.append(self.comment('visit_field'))
        pass

    def depart_field(self, node):
        #self.body.append(self.comment('depart_field'))
        pass

    def visit_field_body(self, node):
        #self.body.append(self.comment('visit_field_body'))
        if self._in_docinfo:
            self._docinfo[
                    self._field_name.lower().replace(" ","_")] = node.astext()
            raise nodes.SkipNode

    def depart_field_body(self, node):
        pass

    def visit_field_list(self, node):
        self.indent(FIELD_LIST_INDENT)

    def depart_field_list(self, node):
        self.dedent('depart_field_list')

    def visit_field_name(self, node):
        if self._in_docinfo:
            self._in_docinfo = 1
            self._field_name = node.astext()
            raise nodes.SkipNode
        else:
            self.body.append(self.defs['field_name'][0])

    def depart_field_name(self, node):
        self.body.append(self.defs['field_name'][1])

    def visit_figure(self, node):
        raise NotImplementedError, node.astext()

    def depart_figure(self, node):
        raise NotImplementedError, node.astext()

    def visit_footer(self, node):
        raise NotImplementedError, node.astext()

    def depart_footer(self, node):
        raise NotImplementedError, node.astext()
        start = self.context.pop()
        footer = (['<hr class="footer"/>\n',
                   self.starttag(node, 'div', CLASS='footer')]
                  + self.body[start:] + ['</div>\n'])
        self.body_suffix[:0] = footer
        del self.body[start:]

    def visit_footnote(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'table', CLASS='footnote',
                                       frame="void", rules="none"))
        self.body.append('<colgroup><col class="label" /><col /></colgroup>\n'
                         '<tbody valign="top">\n'
                         '<tr>')
        self.footnote_backrefs(node)

    def footnote_backrefs(self, node):
        raise NotImplementedError, node.astext()
        if self.settings.footnote_backlinks and node.hasattr('backrefs'):
            backrefs = node['backrefs']
            if len(backrefs) == 1:
                self.context.append('')
                self.context.append('<a class="fn-backref" href="#%s" '
                                    'name="%s">' % (backrefs[0], node['id']))
            else:
                i = 1
                backlinks = []
                for backref in backrefs:
                    backlinks.append('<a class="fn-backref" href="#%s">%s</a>'
                                     % (backref, i))
                    i += 1
                self.context.append('<em>(%s)</em> ' % ', '.join(backlinks))
                self.context.append('<a name="%s">' % node['id'])
        else:
            self.context.append('')
            self.context.append('<a name="%s">' % node['id'])

    def depart_footnote(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('</td></tr>\n'
                         '</tbody>\n</table>\n')

    def visit_footnote_reference(self, node):
        raise NotImplementedError, node.astext()
        href = ''
        if node.has_key('refid'):
            href = '#' + node['refid']
        elif node.has_key('refname'):
            href = '#' + self.document.nameids[node['refname']]
        format = self.settings.footnote_references
        if format == 'brackets':
            suffix = '['
            self.context.append(']')
        elif format == 'superscript':
            suffix = '<sup>'
            self.context.append('</sup>')
        else:                           # shouldn't happen
            suffix = '???'
            self.content.append('???')
        self.body.append(self.starttag(node, 'a', suffix, href=href,
                                       CLASS='footnote-reference'))

    def depart_footnote_reference(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.context.pop() + '</a>')

    def visit_generated(self, node):
        pass

    def depart_generated(self, node):
        pass

    def visit_header(self, node):
        raise NotImplementedError, node.astext()
        self.context.append(len(self.body))

    def depart_header(self, node):
        raise NotImplementedError, node.astext()
        start = self.context.pop()
        self.body_prefix.append(self.starttag(node, 'div', CLASS='header'))
        self.body_prefix.extend(self.body[start:])
        self.body_prefix.append('<hr />\n</div>\n')
        del self.body[start:]

    def visit_hint(self, node):
        self.visit_admonition(node, 'hint')

    def depart_hint(self, node):
        self.depart_admonition()

    def visit_image(self, node):
        raise NotImplementedError, node.astext()
        atts = node.attributes.copy()
        atts['src'] = atts['uri']
        del atts['uri']
        if not atts.has_key('alt'):
            atts['alt'] = atts['src']
        if isinstance(node.parent, nodes.TextElement):
            self.context.append('')
        else:
            self.body.append('<p>')
            self.context.append('</p>\n')
        self.body.append(self.emptytag(node, 'img', '', **atts))

    def depart_image(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.context.pop())

    def visit_important(self, node):
        self.visit_admonition(node, 'important')

    def depart_important(self, node):
        self.depart_admonition()

    def visit_label(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'td', '%s[' % self.context.pop(),
                                       CLASS='label'))

    def depart_label(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(']</a></td><td>%s' % self.context.pop())

    def visit_legend(self, node):
        raise NotImplementedError, node.astext()
        self.body.append(self.starttag(node, 'div', CLASS='legend'))

    def depart_legend(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('</div>\n')

    def visit_line_block(self, node):
        self.body.append('\n')

    def depart_line_block(self, node):
        self.body.append('\n')

    def visit_line(self, node):
        pass

    def depart_line(self, node):
        self.body.append('\n.br\n')

    def visit_list_item(self, node):
        # man 7 man argues to use ".IP" instead of ".TP"
        self.body.append('\n.IP %s %d\n' % (
                self._list_char[-1].next(),
                self._list_char[-1].get_width(),) )

    def depart_list_item(self, node):
        pass

    def visit_literal(self, node):
        self.body.append(self.defs['literal'][0])

    def depart_literal(self, node):
        self.body.append(self.defs['literal'][1])

    def visit_literal_block(self, node):
        self.body.append(self.defs['literal_block'][0])

    def depart_literal_block(self, node):
        self.body.append(self.defs['literal_block'][1])

    def visit_meta(self, node):
        raise NotImplementedError, node.astext()
        self.head.append(self.emptytag(node, 'meta', **node.attributes))

    def depart_meta(self, node):
        pass

    def visit_note(self, node):
        self.visit_admonition(node, 'note')

    def depart_note(self, node):
        self.depart_admonition()

    def indent(self, by=0.5):
        # if we are in a section ".SH" there already is a .RS
        #self.body.append('\n[[debug: listchar: %r]]\n' % map(repr, self._list_char))
        #self.body.append('\n[[debug: indent %r]]\n' % self._indent)
        step = self._indent[-1]
        self._indent.append(by)
        self.body.append(self.defs['indent'][0] % step)

    def dedent(self, name=''):
        #self.body.append('\n[[debug: dedent %s %r]]\n' % (name, self._indent))
        self._indent.pop()
        self.body.append(self.defs['indent'][1])

    def visit_option_list(self, node):
        self.indent(OPTION_LIST_INDENT)

    def depart_option_list(self, node):
        self.dedent()

    def visit_option_list_item(self, node):
        # one item of the list
        self.body.append(self.defs['option_list_item'][0])

    def depart_option_list_item(self, node):
        self.body.append(self.defs['option_list_item'][1])

    def visit_option_group(self, node):
        # as one option could have several forms it is a group
        # options without parameter bold only, .B, -v
        # options with parameter bold italic, .BI, -f file
        
        # we do not know if .B or .BI
        self.context.append('.B')           # blind guess
        self.context.append(len(self.body)) # to be able to insert later
        self.context.append(0)              # option counter

    def depart_option_group(self, node):
        self.context.pop()  # the counter
        start_position = self.context.pop()
        text = self.body[start_position:]
        del self.body[start_position:]
        self.body.append('\n%s%s' % (self.context.pop(), ''.join(text)))

    def visit_option(self, node):
        # each form of the option will be presented separately
        if self.context[-1]>0:
            self.body.append(' ,')
        if self.context[-3] == '.BI':
            self.body.append('\\')
        self.body.append(' ')

    def depart_option(self, node):
        self.context[-1] += 1

    def visit_option_string(self, node):
        # do not know if .B or .BI
        pass

    def depart_option_string(self, node):
        pass

    def visit_option_argument(self, node):
        self.context[-3] = '.BI' # bold/italic alternate
        if node['delimiter'] != ' ':
            self.body.append('\\fn%s ' % node['delimiter'] )
        elif self.body[len(self.body)-1].endswith('='):
            # a blank only means no blank in output, just changing font
            self.body.append(' ')
        else:
            # backslash blank blank
            self.body.append('\\  ')

    def depart_option_argument(self, node):
        pass

    def visit_organization(self, node):
        self._docinfo['organization'] = node.astext()
        raise nodes.SkipNode

    def depart_organization(self, node):
        pass

    def visit_paragraph(self, node):
        # BUG every but the first paragraph in a list must be intended
        # TODO .PP or new line
        return

    def depart_paragraph(self, node):
        # TODO .PP or an empty line
        if not self._in_entry:
            self.body.append('\n\n')

    def visit_problematic(self, node):
        self.body.append(self.defs['problematic'][0])

    def depart_problematic(self, node):
        self.body.append(self.defs['problematic'][1])

    def visit_raw(self, node):
        if node.get('format') == 'manpage':
            self.body.append(node.astext())
        # Keep non-manpage raw text out of output:
        raise nodes.SkipNode

    def visit_reference(self, node):
        """E.g. link or email address."""
        self.body.append(self.defs['reference'][0])

    def depart_reference(self, node):
        self.body.append(self.defs['reference'][1])

    def visit_revision(self, node):
        self.visit_docinfo_item(node, 'revision')

    def depart_revision(self, node):
        self.depart_docinfo_item()

    def visit_row(self, node):
        self._active_table.new_row()

    def depart_row(self, node):
        pass

    def visit_section(self, node):
        self.section_level += 1

    def depart_section(self, node):
        self.section_level -= 1    

    def visit_status(self, node):
        raise NotImplementedError, node.astext()
        self.visit_docinfo_item(node, 'status', meta=None)

    def depart_status(self, node):
        self.depart_docinfo_item()

    def visit_strong(self, node):
        self.body.append(self.defs['strong'][1])

    def depart_strong(self, node):
        self.body.append(self.defs['strong'][1])

    def visit_substitution_definition(self, node):
        """Internal only."""
        raise nodes.SkipNode

    def visit_substitution_reference(self, node):
        self.unimplemented_visit(node)

    def visit_subtitle(self, node):
        self._docinfo["subtitle"] = node.astext()
        raise nodes.SkipNode

    def visit_system_message(self, node):
        # TODO add report_level
        #if node['level'] < self.document.reporter['writer'].report_level:
            # Level is too low to display:
        #    raise nodes.SkipNode
        self.body.append('\.SH system-message\n')
        attr = {}
        backref_text = ''
        if node.hasattr('id'):
            attr['name'] = node['id']
        if node.hasattr('line'):
            line = ', line %s' % node['line']
        else:
            line = ''
        self.body.append('System Message: %s/%s (%s:%s)\n'
                         % (node['type'], node['level'], node['source'], line))

    def depart_system_message(self, node):
        self.body.append('\n')

    def visit_table(self, node):
        self._active_table = Table()

    def depart_table(self, node):
        self.body.append(self._active_table.astext())
        self._active_table = None

    def visit_target(self, node):
        self.body.append(self.comment('visit_target'))
        #self.body.append(self.defs['target'][0])
        #self.body.append(node['refuri'])

    def depart_target(self, node):
        self.body.append(self.comment('depart_target'))
        #self.body.append(self.defs['target'][1])

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    def visit_term(self, node):
        self.body.append(self.defs['term'][0])

    def depart_term(self, node):
        self.body.append(self.defs['term'][1])

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_compound(self, node):
        pass

    def depart_compound(self, node):
        pass

    def visit_thead(self, node):
        raise NotImplementedError, node.astext()
        self.write_colspecs()
        self.body.append(self.context.pop()) # '</colgroup>\n'
        # There may or may not be a <thead>; this is for <tbody> to use:
        self.context.append('')
        self.body.append(self.starttag(node, 'thead', valign='bottom'))

    def depart_thead(self, node):
        raise NotImplementedError, node.astext()
        self.body.append('</thead>\n')

    def visit_tip(self, node):
        self.visit_admonition(node, 'tip')

    def depart_tip(self, node):
        self.depart_admonition()

    def visit_title(self, node):
        if isinstance(node.parent, nodes.topic):
            self.body.append(self.comment('topic-title'))
        elif isinstance(node.parent, nodes.sidebar):
            self.body.append(self.comment('sidebar-title'))
        elif isinstance(node.parent, nodes.admonition):
            self.body.append(self.comment('admonition-title'))
        elif self.section_level == 0:
            # document title for .TH
            self._docinfo['title'] = node.astext()
            raise nodes.SkipNode
        elif self.section_level == 1:
            self._docinfo['subtitle'] = node.astext()
            raise nodes.SkipNode
        elif self.section_level == 2:
            self.body.append('\n.SH ')
        else:
            self.body.append('\n.SS ')

    def depart_title(self, node):
        self.body.append('\n')

    def visit_title_reference(self, node):
        """inline citation reference"""
        self.body.append(self.defs['title_reference'][0])

    def depart_title_reference(self, node):
        self.body.append(self.defs['title_reference'][1])

    def visit_topic(self, node):
        self.body.append(self.comment('topic: '+node.astext()))
        raise nodes.SkipNode
        ##self.topic_class = node.get('class')

    def depart_topic(self, node):
        ##self.topic_class = ''
        pass

    def visit_transition(self, node):
        # .PP      Begin a new paragraph and reset prevailing indent.
        # .sp N    leaves N lines of blank space.
        # .ce      centers the next line
        self.body.append('\n.sp\n.ce\n----\n')

    def depart_transition(self, node):
        self.body.append('\n.ce 0\n.sp\n')

    def visit_version(self, node):
        self._docinfo["version"] = node.astext()
        raise nodes.SkipNode

    def visit_warning(self, node):
        self.visit_admonition(node, 'warning')

    def depart_warning(self, node):
        self.depart_admonition()

    def visit_index(self, node):
        pass

    def depart_index(self, node):
        pass

    def visit_desc(self, node):
        pass

    def depart_desc(self, node):
        pass

    def visit_desc_signature(self, node):
        # .. cmdoption makes options look like this
        self.body.append('\n')
        self.body.append('.TP')
        self.body.append('\n')

    def depart_desc_signature(self, node):
        pass

    def visit_desc_name(self, node):
        self.body.append(r'\fB') # option name

    def depart_desc_name(self, node):
        self.body.append(r'\fR')

    def visit_desc_addname(self, node):
        self.body.append(r'\fR')

    def depart_desc_addname(self, node):
        # self.body.append(r'\fR')
        pass

    def visit_desc_content(self, node):
        self.body.append('\n') # option help

    def depart_desc_content(self, node):
        pass

    def unimplemented_visit(self, node):
        pass

# vim: set et ts=4 ai :
