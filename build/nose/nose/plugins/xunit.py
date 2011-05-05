
"""This plugin provides test results in the standard XUnit XML format.

It was designed for the `Hudson`_ continuous build system but will
probably work for anything else that understands an XUnit-formatted XML
representation of test results.

Add this shell command to your builder ::

    nosetests --with-xunit

And by default a file named nosetests.xml will be written to the
working directory.

In a Hudson builder, tick the box named "Publish JUnit test result report"
under the Post-build Actions and enter this value for Test report XMLs::

    **/nosetests.xml

If you need to change the name or location of the file, you can set the
``--xunit-file`` option.

Here is an abbreviated version of what an XML test report might look like::

    <?xml version="1.0" encoding="UTF-8"?>
    <testsuite name="nosetests" tests="1" errors="1" failures="0" skip="0">
        <testcase classname="path_to_test_suite.TestSomething"
                  name="test_it" time="0">
            <error type="exceptions.TypeError" message="oops, wrong type">
            Traceback (most recent call last):
            ...
            TypeError: oops, wrong type
            </error>
        </testcase>
    </testsuite>

.. _Hudson: https://hudson.dev.java.net/

"""

import doctest
import os
import traceback
import re
import inspect
from nose.plugins.base import Plugin
from nose.exc import SkipTest
from time import time
from xml.sax import saxutils
from nose.pyversion import UNICODE_STRINGS

# Invalid XML characters, control characters 0-31 sans \t, \n and \r
CONTROL_CHARACTERS = re.compile(r"[\000-\010\013\014\016-\037]")

def xml_safe(value):
    """Replaces invalid XML characters with '?'."""
    return CONTROL_CHARACTERS.sub('?', value)

def escape_cdata(cdata):
    """Escape a string for an XML CDATA section."""
    return xml_safe(cdata).replace(']]>', ']]>]]&gt;<![CDATA[')

def nice_classname(obj):
    """Returns a nice name for class object or class instance.

        >>> nice_classname(Exception()) # doctest: +ELLIPSIS
        '...Exception'
        >>> nice_classname(Exception) # doctest: +ELLIPSIS
        '...Exception'

    """
    if inspect.isclass(obj):
        cls_name = obj.__name__
    else:
        cls_name = obj.__class__.__name__
    mod = inspect.getmodule(obj)
    if mod:
        name = mod.__name__
        # jython
        if name.startswith('org.python.core.'):
            name = name[len('org.python.core.'):]
        return "%s.%s" % (name, cls_name)
    else:
        return cls_name

def exc_message(exc_info):
    """Return the exception's message."""
    exc = exc_info[1]
    if exc is None:
        # str exception
        result = exc_info[0]
    else:
        try:
            result = str(exc)
        except UnicodeEncodeError:
            try:
                result = unicode(exc)
            except UnicodeError:
                # Fallback to args as neither str nor
                # unicode(Exception(u'\xe6')) work in Python < 2.6
                result = exc.args[0]
    return xml_safe(result)

class Xunit(Plugin):
    """This plugin provides test results in the standard XUnit XML format."""
    name = 'xunit'
    score = 2000
    encoding = 'UTF-8'
    error_report_file = None

    def _timeTaken(self):
        if hasattr(self, '_timer'):
            taken = time() - self._timer
        else:
            # test died before it ran (probably error in setup())
            # or success/failure added before test started probably 
            # due to custom TestResult munging
            taken = 0.0
        return taken

    def _quoteattr(self, attr):
        """Escape an XML attribute. Value can be unicode."""
        attr = xml_safe(attr)
        if isinstance(attr, unicode) and not UNICODE_STRINGS:
            attr = attr.encode(self.encoding)
        return saxutils.quoteattr(attr)

    def options(self, parser, env):
        """Sets additional command line options."""
        Plugin.options(self, parser, env)
        parser.add_option(
            '--xunit-file', action='store',
            dest='xunit_file', metavar="FILE",
            default=env.get('NOSE_XUNIT_FILE', 'nosetests.xml'),
            help=("Path to xml file to store the xunit report in. "
                  "Default is nosetests.xml in the working directory "
                  "[NOSE_XUNIT_FILE]"))

    def configure(self, options, config):
        """Configures the xunit plugin."""
        Plugin.configure(self, options, config)
        self.config = config
        if self.enabled:
            self.stats = {'errors': 0,
                          'failures': 0,
                          'passes': 0,
                          'skipped': 0
                          }
            self.errorlist = []
            if UNICODE_STRINGS:
                self.error_report_file = open(options.xunit_file, 'w', encoding=self.encoding)
            else:
                self.error_report_file = open(options.xunit_file, 'w')

    def report(self, stream):
        """Writes an Xunit-formatted XML file

        The file includes a report of test errors and failures.

        """
        self.stats['encoding'] = self.encoding
        self.stats['total'] = (self.stats['errors'] + self.stats['failures']
                               + self.stats['passes'] + self.stats['skipped'])
        self.error_report_file.write(
            '<?xml version="1.0" encoding="%(encoding)s"?>'
            '<testsuite name="nosetests" tests="%(total)d" '
            'errors="%(errors)d" failures="%(failures)d" '
            'skip="%(skipped)d">' % self.stats)
        self.error_report_file.write(''.join(self.errorlist))
        self.error_report_file.write('</testsuite>')
        self.error_report_file.close()
        if self.config.verbosity > 1:
            stream.writeln("-" * 70)
            stream.writeln("XML: %s" % self.error_report_file.name)

    def startTest(self, test):
        """Initializes a timer before starting a test."""
        self._timer = time()

    def addError(self, test, err, capt=None):
        """Add error output to Xunit report.
        """
        taken = self._timeTaken()

        if issubclass(err[0], SkipTest):
            type = 'skipped'
            self.stats['skipped'] += 1
        else:
            type = 'error'
            self.stats['errors'] += 1
        tb = ''.join(traceback.format_exception(*err))
        id = test.id()
        self.errorlist.append(
            '<testcase classname=%(cls)s name=%(name)s time="%(taken)d">'
            '<%(type)s type=%(errtype)s message=%(message)s><![CDATA[%(tb)s]]>'
            '</%(type)s></testcase>' %
            {'cls': self._quoteattr('.'.join(id.split('.')[:-1])),
             'name': self._quoteattr(id.split('.')[-1]),
             'taken': taken,
             'type': type,
             'errtype': self._quoteattr(nice_classname(err[0])),
             'message': self._quoteattr(exc_message(err)),
             'tb': escape_cdata(tb),
             })

    def addFailure(self, test, err, capt=None, tb_info=None):
        """Add failure output to Xunit report.
        """
        taken = self._timeTaken()
        tb = ''.join(traceback.format_exception(*err))
        self.stats['failures'] += 1
        id = test.id()
        self.errorlist.append(
            '<testcase classname=%(cls)s name=%(name)s time="%(taken)d">'
            '<failure type=%(errtype)s message=%(message)s><![CDATA[%(tb)s]]>'
            '</failure></testcase>' %
            {'cls': self._quoteattr('.'.join(id.split('.')[:-1])),
             'name': self._quoteattr(id.split('.')[-1]),
             'taken': taken,
             'errtype': self._quoteattr(nice_classname(err[0])),
             'message': self._quoteattr(exc_message(err)),
             'tb': escape_cdata(tb),
             })

    def addSuccess(self, test, capt=None):
        """Add success output to Xunit report.
        """
        taken = self._timeTaken()
        self.stats['passes'] += 1
        id = test.id()
        self.errorlist.append(
            '<testcase classname=%(cls)s name=%(name)s '
            'time="%(taken)d" />' %
            {'cls': self._quoteattr('.'.join(id.split('.')[:-1])),
             'name': self._quoteattr(id.split('.')[-1]),
             'taken': taken,
             })
