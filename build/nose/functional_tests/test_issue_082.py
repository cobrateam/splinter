import os
import re
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
import unittest

from nose.plugins import Plugin, PluginTester
from nose.plugins.builtin import FailureDetail, Capture, Doctest

support = os.path.join(os.path.dirname(__file__), 'support')


class IncludeUnderscoreFilesPlugin(Plugin):

    # Note that this is purely for purposes of testing nose itself, and is
    # not intended to be a useful plugin.  In particular, the rules it
    # applies for _*.py files differ from the nose defaults (e.g. the
    # --testmatch option is ignored).

    name = "underscorefiles"

    def wantFile(self, file):
        base = os.path.basename(file)
        dummy, ext = os.path.splitext(base)
        pysrc = ext == '.py'
        if pysrc and os.path.basename(file).startswith("_"):
            return True

    def wantDirectory(self, dirname):
        if os.path.basename(dirname).startswith("_"):
            return True


class TestIncludeUnderscoreFiles(PluginTester, unittest.TestCase):
    activate = '--with-underscorefiles'
    plugins = [IncludeUnderscoreFilesPlugin(), Doctest()]
    args = ['-v', '--with-doctest']
    suitepath = os.path.join(support, 'issue082')
    ignoreFiles = (re.compile(r'^\.'),
                   # we want _*.py, but don't want e.g. __init__.py, since that
                   # appears to cause infinite recursion at the moment
                   re.compile(r'^__'),
                   re.compile(r'^setup\.py$')
                   )

    def test_assert_info_in_output(self):
        print self.output
        # In future, all four test cases will be run.  Backwards-compatibility
        # means that can't be done in nose 0.10.
        assert '_mypackage._eggs' not in str(self.output)
        assert '_mypackage.bacon' not in str(self.output)
        assert 'Doctest: mypublicpackage._foo ... FAIL' in str(self.output)
        assert 'Doctest: mypublicpackage.bar ... FAIL' in str(self.output)


class TestExcludeUnderscoreFilesByDefault(PluginTester, unittest.TestCase):
    activate = '-v'
    plugins = [Doctest()]
    args = ['--with-doctest']
    suitepath = os.path.join(support, 'issue082')

    def test_assert_info_in_output(self):
        print self.output
        assert '_mypackage._eggs' not in str(self.output)
        assert '_mypackage.bacon' not in str(self.output)
        assert 'mypublicpackage._foo' not in str(self.output)
        assert 'Doctest: mypublicpackage.bar ... FAIL' in str(self.output)


if __name__ == '__main__':
    unittest.main()
