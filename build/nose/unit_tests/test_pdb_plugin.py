import sys
import unittest
from nose.config import Config
from nose.plugins import debug
from optparse import OptionParser
from StringIO import StringIO

class StubPdb:
    called = False
    def post_mortem(self, tb):
        self.called = True

class TestPdbPlugin(unittest.TestCase):

    def setUp(self):
        self._pdb = debug.pdb
        self._so = sys.stdout
        debug.pdb = StubPdb()

    def tearDown(self):
        debug.pdb = self._pdb
        sys.stdout = self._so

    def test_plugin_api(self):
        p = debug.Pdb()
        p.addOptions
        p.configure
        p.addError
        p.addFailure

    def test_plugin_calls_pdb(self):
        p = debug.Pdb()

        try:
            raise Exception("oops")
        except:
            err = sys.exc_info()
    
        p.enabled = True
        p.enabled_for_errors = True
        p.enabled_for_failures = True

        p.addError(None, err)
        assert debug.pdb.called, "Did not call pdb.post_mortem on error"

        debug.pdb.called = False
        p.addFailure(None, err)
        assert debug.pdb.called, "Did not call pdb.post_mortem on failure"

    def test_command_line_options_enable(self):
        parser = OptionParser()

        p = debug.Pdb()
        p.addOptions(parser)
        options, args = parser.parse_args(['test_configuration',
                                           '--pdb',
                                           '--pdb-failures'])
        p.configure(options, Config())
        assert p.enabled
        assert p.enabled_for_errors
        assert p.enabled_for_failures

    def test_disabled_by_default(self):
        p = debug.Pdb()
        assert not p.enabled
        assert not p.enabled_for_failures

        parser = OptionParser()
        p.addOptions(parser)
        options, args = parser.parse_args(['test_configuration'])
        p.configure(options, Config())
        assert not p.enabled
        assert not p.enabled_for_errors
        assert not p.enabled_for_failures
        
    def test_env_settings_enable(self):
        p = debug.Pdb()
        assert not p.enabled
        assert not p.enabled_for_failures

        env = {'NOSE_PDB': '1',
               'NOSE_PDB_FAILURES': '1'}

        parser = OptionParser()
        p.addOptions(parser, env)
        options, args = parser.parse_args(['test_configuration'])
        p.configure(options, Config())
        assert p.enabled
        assert p.enabled_for_errors
        assert p.enabled_for_failures

    def test_real_stdout_restored_before_call(self):
        
        class CheckStdout(StubPdb):
            def post_mortem(self, tb):
                assert sys.stdout is sys.__stdout__, \
                       "sys.stdout was not restored to sys.__stdout__ " \
                       "before call"
        debug.pdb = CheckStdout()

        patch = StringIO()
        sys.stdout = patch
        p = debug.Pdb()
        p.enabled = True
        p.enabled_for_errors = True

        try:
            raise Exception("oops")
        except:
            err = sys.exc_info()
    
        p.addError(None, err)    
        assert sys.stdout is patch, "sys.stdout was not reset after call"
        
        
if __name__ == '__main__':
    unittest.main()
