import os
import sys
import unittest
from difflib import ndiff
from cStringIO import StringIO

from nose.config import Config
from nose.plugins.manager import PluginManager
from nose.plugins.skip import Skip
from nose import loader
from nose import suite
from nose.result import _TextTestResult
try:
    # 2.7+
    from unittest.runner import _WritelnDecorator
except ImportError:
    from unittest import _WritelnDecorator

support = os.path.abspath(os.path.join(os.path.dirname(__file__), 'support'))

class TestNoseTestLoader(unittest.TestCase):

    def setUp(self):
        self._mods = sys.modules.copy()
        suite.ContextSuiteFactory.suiteClass = TreePrintContextSuite

    def tearDown(self):
        to_del = [ m for m in sys.modules.keys() if
                   m not in self._mods ]
        if to_del:
            for mod in to_del:
                del sys.modules[mod]
        sys.modules.update(self._mods)
        suite.ContextSuiteFactory.suiteClass = suite.ContextSuite

    def test_load_from_name_file(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package1')
        l = loader.TestLoader(workingDir=wd)

        file_suite = l.loadTestsFromName('tests/test_example_function.py')
        file_suite(res)
        assert not res.errors, res.errors
        assert not res.failures, res.failures

    def test_load_from_name_dot(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package1')
        l = loader.TestLoader(workingDir=wd)
        dir_suite = l.loadTestsFromName('.')
        dir_suite(res)
        assert not res.errors, res.errors
        assert not res.failures, res.failures

    def test_load_from_name_file_callable(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package1')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromName(
            'tests/test_example_function.py:test_times_two')
        suite(res)
        assert not res.errors, res.errors
        assert not res.failures, res.failures
        self.assertEqual(res.testsRun, 1)

    def test_fixture_context(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package2')
        l = loader.TestLoader(workingDir=wd)
        dir_suite = l.loadTestsFromName('.')
        dir_suite(res)

        m = sys.modules['test_pak']
        print "test pak state", m.state

        assert not res.errors, res.errors
        assert not res.failures, res.failures
        self.assertEqual(res.testsRun, 5)

        # Expected order of calls
        expect = ['test_pak.setup',
                  'test_pak.test_mod.setup',
                  'test_pak.test_mod.test_add',
                  'test_pak.test_mod.test_minus',
                  'test_pak.test_mod.teardown',
                  'test_pak.test_sub.setup',
                  'test_pak.test_sub.test_mod.setup',
                  'test_pak.test_sub.test_mod.TestMaths.setup_class',
                  'test_pak.test_sub.test_mod.TestMaths.setup',
                  'test_pak.test_sub.test_mod.TestMaths.test_div',
                  'test_pak.test_sub.test_mod.TestMaths.teardown',
                  'test_pak.test_sub.test_mod.TestMaths.setup',
                  'test_pak.test_sub.test_mod.TestMaths.test_two_two',
                  'test_pak.test_sub.test_mod.TestMaths.teardown',
                  'test_pak.test_sub.test_mod.TestMaths.teardown_class',
                  'test_pak.test_sub.test_mod.test',
                  'test_pak.test_sub.test_mod.teardown',
                  'test_pak.test_sub.teardown',
                  'test_pak.teardown']
        self.assertEqual(len(m.state), len(expect))
        for item in m.state:
            self.assertEqual(item, expect.pop(0))

    def test_fixture_context_name_is_module(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package2')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromName('test_pak.test_mod')
        suite(res)

        assert 'test_pak' in sys.modules, \
               "Context did not load test_pak"
        m = sys.modules['test_pak']
        print "test pak state", m.state
        expect = ['test_pak.setup',
                  'test_pak.test_mod.setup',
                  'test_pak.test_mod.test_add',
                  'test_pak.test_mod.test_minus',
                  'test_pak.test_mod.teardown',
                  'test_pak.teardown']
        self.assertEqual(len(m.state), len(expect))
        for item in m.state:
            self.assertEqual(item, expect.pop(0))

    def test_fixture_context_name_is_test_function(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package2')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromName('test_pak.test_mod:test_add')
        suite(res)

        assert 'test_pak' in sys.modules, \
               "Context did not load test_pak"
        m = sys.modules['test_pak']
        print "test pak state", m.state
        expect = ['test_pak.setup',
                  'test_pak.test_mod.setup',
                  'test_pak.test_mod.test_add',
                  'test_pak.test_mod.teardown',
                  'test_pak.teardown']
        self.assertEqual(len(m.state), len(expect))
        for item in m.state:
            self.assertEqual(item, expect.pop(0))

    def test_fixture_context_name_is_test_class(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package2')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromName(
            'test_pak.test_sub.test_mod:TestMaths')
        suite(res)

        assert 'test_pak' in sys.modules, \
               "Context did not load test_pak"
        m = sys.modules['test_pak']
        # print "test pak state", m.state
        expect = ['test_pak.setup',
                  'test_pak.test_sub.setup',
                  'test_pak.test_sub.test_mod.setup',
                  'test_pak.test_sub.test_mod.TestMaths.setup_class',
                  'test_pak.test_sub.test_mod.TestMaths.setup',
                  'test_pak.test_sub.test_mod.TestMaths.test_div',
                  'test_pak.test_sub.test_mod.TestMaths.teardown',
                  'test_pak.test_sub.test_mod.TestMaths.setup',
                  'test_pak.test_sub.test_mod.TestMaths.test_two_two',
                  'test_pak.test_sub.test_mod.TestMaths.teardown',
                  'test_pak.test_sub.test_mod.TestMaths.teardown_class',
                  'test_pak.test_sub.test_mod.teardown',
                  'test_pak.test_sub.teardown',
                  'test_pak.teardown']
        self.assertEqual(m.state, expect, diff(expect, m.state))

    def test_fixture_context_name_is_test_class_test(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package2')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromName(
            'test_pak.test_sub.test_mod:TestMaths.test_div')
        suite(res)

        assert 'test_pak' in sys.modules, \
               "Context not load test_pak"
        m = sys.modules['test_pak']
        print "test pak state", m.state
        expect = ['test_pak.setup',
                  'test_pak.test_sub.setup',
                  'test_pak.test_sub.test_mod.setup',
                  'test_pak.test_sub.test_mod.TestMaths.setup_class',
                  'test_pak.test_sub.test_mod.TestMaths.setup',
                  'test_pak.test_sub.test_mod.TestMaths.test_div',
                  'test_pak.test_sub.test_mod.TestMaths.teardown',
                  'test_pak.test_sub.test_mod.TestMaths.teardown_class',
                  'test_pak.test_sub.test_mod.teardown',
                  'test_pak.test_sub.teardown',
                  'test_pak.teardown']
        self.assertEqual(m.state, expect, diff(expect, m.state))

    def test_fixture_context_multiple_names(self):
        res = unittest.TestResult()
        wd = os.path.join(support, 'package2')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromNames(
            ['test_pak.test_sub.test_mod:TestMaths.test_div',
             'test_pak.test_sub.test_mod:TestMaths.test_two_two',
             'test_pak.test_mod:test_add'])
        print suite
        suite(res)
        assert not res.errors, res.errors
        assert not res.failures, res.failures
        assert 'test_pak' in sys.modules, \
               "Context not load test_pak"
        m = sys.modules['test_pak']
        print "test pak state", m.state
        expect = ['test_pak.setup',
                  'test_pak.test_sub.setup',
                  'test_pak.test_sub.test_mod.setup',
                  'test_pak.test_sub.test_mod.TestMaths.setup_class',
                  'test_pak.test_sub.test_mod.TestMaths.setup',
                  'test_pak.test_sub.test_mod.TestMaths.test_div',
                  'test_pak.test_sub.test_mod.TestMaths.teardown',
                  'test_pak.test_sub.test_mod.TestMaths.setup',
                  'test_pak.test_sub.test_mod.TestMaths.test_two_two',
                  'test_pak.test_sub.test_mod.TestMaths.teardown',
                  'test_pak.test_sub.test_mod.TestMaths.teardown_class',
                  'test_pak.test_sub.test_mod.teardown',
                  'test_pak.test_sub.teardown',
                  'test_pak.test_mod.setup',
                  'test_pak.test_mod.test_add',
                  'test_pak.test_mod.teardown',
                  'test_pak.teardown']
        self.assertEqual(m.state, expect, diff(expect, m.state))

    def test_fixture_context_multiple_names_some_common_ancestors(self):
        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, 2)
        wd = os.path.join(support, 'ltfn')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromNames(
            ['test_pak1.test_mod',
             'test_pak2:test_two_two',
             'test_pak1:test_one_one'])
        print suite
        suite(res)
        res.printErrors()
        print stream.getvalue()
        assert not res.errors, res.errors
        assert not res.failures, res.failures
        assert 'state' in sys.modules, \
               "Context not load state module"
        m = sys.modules['state']
        print "state", m.called

        expect = ['test_pak1.setup',
                  'test_pak1.test_mod.setup',
                  'test_pak1.test_mod.test_one_mod_one',
                  'test_pak1.test_mod.teardown',
                  'test_pak1.test_one_one',
                  'test_pak1.teardown',
                  'test_pak2.setup',
                  'test_pak2.test_two_two',
                  'test_pak2.teardown']
        self.assertEqual(m.called, expect, diff(expect, m.called))

    def test_fixture_context_multiple_names_no_common_ancestors(self):
        stream = _WritelnDecorator(StringIO())
        res = _TextTestResult(stream, 0, 2)
        wd = os.path.join(support, 'ltfn')
        l = loader.TestLoader(workingDir=wd)
        suite = l.loadTestsFromNames(
            ['test_pak1.test_mod',
             'test_pak2:test_two_two',
             'test_mod'])
        print suite
        suite(res)
        res.printErrors()
        print stream.getvalue()
        assert not res.errors, res.errors
        assert not res.failures, res.failures
        assert 'state' in sys.modules, \
               "Context not load state module"
        m = sys.modules['state']
        print "state", m.called

        expect = ['test_pak1.setup',
                  'test_pak1.test_mod.setup',
                  'test_pak1.test_mod.test_one_mod_one',
                  'test_pak1.test_mod.teardown',
                  'test_pak1.teardown',
                  'test_pak2.setup',
                  'test_pak2.test_two_two',
                  'test_pak2.teardown',
                  'test_mod.setup',
                  'test_mod.test_mod',
                  'test_mod.teardown']
        self.assertEqual(m.called, expect, diff(expect, m.called))
    
    def test_mod_setup_fails_no_tests_run(self):
        ctx = os.path.join(support, 'ctx')
        l = loader.TestLoader(workingDir=ctx)
        suite = l.loadTestsFromName('mod_setup_fails.py')

        res = unittest.TestResult()
        suite(res)

        assert res.errors
        assert not res.failures, res.failures
        assert res.testsRun == 0, \
               "Expected to run 0 tests but ran %s" % res.testsRun

    def test_mod_setup_skip_no_tests_run_no_errors(self):
        config = Config(plugins=PluginManager(plugins=[Skip()]))
        ctx = os.path.join(support, 'ctx')
        l = loader.TestLoader(workingDir=ctx, config=config)
        suite = l.loadTestsFromName('mod_setup_skip.py')

        res = unittest.TestResult()
        suite(res)

        assert not suite.was_setup, "Suite setup did not fail"
        assert not res.errors, res.errors
        assert not res.failures, res.failures
        assert res.skipped
        assert res.testsRun == 0, \
               "Expected to run 0 tests but ran %s" % res.testsRun

    def test_mod_import_skip_one_test_no_errors(self):
        config = Config(plugins=PluginManager(plugins=[Skip()]))
        ctx = os.path.join(support, 'ctx')
        l = loader.TestLoader(workingDir=ctx, config=config)
        suite = l.loadTestsFromName('mod_import_skip.py')

        res = unittest.TestResult()
        suite(res)

        assert not res.errors, res.errors
        assert not res.failures, res.failures
        assert res.testsRun == 1, \
               "Expected to run 1 tests but ran %s" % res.testsRun

    def test_failed_import(self):
        ctx = os.path.join(support, 'ctx')
        l = loader.TestLoader(workingDir=ctx)
        suite = l.loadTestsFromName('no_such_module.py')

        res = _TextTestResult(
            stream=_WritelnDecorator(sys.stdout),
            descriptions=0, verbosity=1)
        suite(res)

        print res.errors
        res.printErrors()
        assert res.errors, "Expected errors but got none"
        assert not res.failures, res.failures
        assert res.testsRun == 1, \
               "Expected to run 1 tests but ran %s" % res.testsRun

    def test_failed_import_module_name(self):
        ctx = os.path.join(support, 'ctx')
        l = loader.TestLoader(workingDir=ctx)
        suite = l.loadTestsFromName('no_such_module')

        res = _TextTestResult(
            stream=_WritelnDecorator(sys.stdout),
            descriptions=0, verbosity=1)
        suite(res)
        print res.errors
        res.printErrors()
        assert res.errors, "Expected errors but got none"
        assert not res.failures, res.failures
        err = res.errors[0][0].test.exc_class
        assert err is ImportError, \
            "Expected import error, got %s" % err

    def test_load_nonsense_name(self):
        ctx = os.path.join(support, 'ctx')
        l = loader.TestLoader(workingDir=ctx)
        suite = l.loadTestsFromName('fred!')

        res = _TextTestResult(
            stream=_WritelnDecorator(sys.stdout),
            descriptions=0, verbosity=1)
        suite(res)
        print res.errors
        assert res.errors, "Expected errors but got none"
        assert not res.failures, res.failures

    def test_generator_with_closure(self):
        """Test that a generator test can employ a closure

        Issue #3. If the generator binds early, the last value
        of the closure will be seen for each generated test and
        the tests will fail.
        """
        gen = os.path.join(support, 'gen')
        l = loader.TestLoader(workingDir=gen)
        suite = l.loadTestsFromName('test')
        res = _TextTestResult(
            stream=_WritelnDecorator(sys.stdout),
            descriptions=0, verbosity=1)
        suite(res)
        assert not res.errors
        self.assertEqual(res.testsRun, 5)

    def test_issue_269(self):
        """Test classes that raise exceptions in __init__ do not stop test run
        """
        wdir = os.path.join(support, 'issue269')
        l = loader.TestLoader(workingDir=wdir)
        suite = l.loadTestsFromName('test_bad_class')
        res = _TextTestResult(
            stream=_WritelnDecorator(sys.stdout),
            descriptions=0, verbosity=1)
        suite(res)
        print res.errors
        self.assertEqual(len(res.errors), 1)
        assert 'raise Exception("pow")' in res.errors[0][1]
        
        
# used for comparing lists
def diff(a, b):
    return '\n' + '\n'.join([ l for l in ndiff(a, b)
                              if not l.startswith('  ') ])


# used for context debugging
class TreePrintContextSuite(suite.ContextSuite):
    indent = ''

    def setUp(self):
        print self, 'setup -->'
        suite.ContextSuite.setUp(self)
        TreePrintContextSuite.indent += '  '

    def tearDown(self):
        TreePrintContextSuite.indent = TreePrintContextSuite.indent[:-2]
        try:
            suite.ContextSuite.tearDown(self)
        finally:
            print self, 'teardown <--'
    def __repr__(self):
        
        return '%s<%s>' % (self.indent,
                           getattr(self.context, '__name__', self.context))
    __str__ = __repr__

        
if __name__ == '__main__':
    #import logging
    #logging.basicConfig() #level=logging.DEBUG)
    #logging.getLogger('nose.suite').setLevel(logging.DEBUG)
    unittest.main()
