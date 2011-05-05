import os
import unittest
from cStringIO import StringIO
from nose import SkipTest
from nose.core import TestProgram
from nose.config import Config
from nose.plugins.manager import DefaultPluginManager
from nose.result import _TextTestResult

here = os.path.dirname(__file__)
support = os.path.join(here, 'support')

class TestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        self.result = _TextTestResult(
            self.stream, self.descriptions, self.verbosity)
        return self.result 

# Note that all of these tests use a set config to avoid the loading
# of plugins or settings from .noserc.

class TestTestProgram(unittest.TestCase):

    def test_run_support_ctx(self):
        """Collect and run tests in functional_tests/support/ctx

        This should collect no tests in the default configuration, since
        none of the modules have test-like names.
        """
        stream = StringIO()
        runner = TestRunner(stream=stream)
        prog = TestProgram(defaultTest=os.path.join(support, 'ctx'),
                           argv=['test_run_support_ctx'],
                           testRunner=runner,
                           config=Config(),
                           exit=False)
        res = runner.result
        print stream.getvalue()
        self.assertEqual(res.testsRun, 0,
                         "Expected to run 0 tests, ran %s" % res.testsRun)
        assert res.wasSuccessful()
        assert not res.errors
        assert not res.failures

    def test_run_support_package2(self):
        """Collect and run tests in functional_tests/support/package2

        This should collect and run 5 tests.
        """
        stream = StringIO()
        runner = TestRunner(stream=stream)
        prog = TestProgram(defaultTest=os.path.join(support, 'package2'),
                           argv=['test_run_support_package2', '-v'],
                           testRunner=runner,
                           config=Config(),
                           exit=False)
        res = runner.result
        print stream.getvalue()
        self.assertEqual(res.testsRun, 5,
                         "Expected to run 5 tests, ran %s" % res.testsRun)
        assert res.wasSuccessful()
        assert not res.errors
        assert not res.failures
        
    def test_run_support_package3(self):
        """Collect and run tests in functional_tests/support/package3

        This should collect and run 2 test. The package layout is:

        lib/
          a.py
        src/
          b.py
        tests/
          test_a.py
          test_b.py
        """
        stream = StringIO()
        runner = TestRunner(stream=stream)

        prog = TestProgram(defaultTest=os.path.join(support, 'package3'),
                           argv=['test_run_support_package3', '-v'],
                           testRunner=runner,
                           config=Config(),
                           exit=False)
        res = runner.result
        print stream.getvalue()
        self.assertEqual(res.testsRun, 2,
                         "Expected to run 2 tests, ran %s" % res.testsRun)
        assert res.wasSuccessful()
        assert not res.errors
        assert not res.failures

    def test_run_support_twist(self):
        """Collect and run tests in functional/support/twist

        This should collect and run 4 tests with 2 fails and an error.
        """
        try:
            from twisted.trial.unittest import TestCase
        except ImportError:
            raise SkipTest('twisted not available; skipping')
        stream = StringIO()
        runner = TestRunner(stream=stream, verbosity=2)

        prog = TestProgram(defaultTest=os.path.join(support, 'twist'),
                           argv=['test_run_support_twist'],
                           testRunner=runner,
                           config=Config(stream=stream),
                           exit=False)
        res = runner.result
        print stream.getvalue()

        # some versions of twisted.trial.unittest.TestCase have
        # runTest in the base class -- this is wrong! But we have
        # to deal with it
        if hasattr(TestCase, 'runTest'):
            expect = 5
        else:
            expect = 4
        self.assertEqual(res.testsRun, expect,
                         "Expected to run %s tests, ran %s" %
                         (expect, res.testsRun))
        assert not res.wasSuccessful()
        assert len(res.errors) == 1
        assert len(res.failures) == 2

    def test_issue_130(self):
        """Collect and run tests in support/issue130 without error.

        This tests that the result and error classes can handle string
        exceptions.
        """
        import warnings
        warnings.filterwarnings('ignore', category=DeprecationWarning,
                                module='test')
        
        stream = StringIO()
        runner = TestRunner(stream=stream, verbosity=2)

        prog = TestProgram(defaultTest=os.path.join(support, 'issue130'),
                           argv=['test_issue_130'],
                           testRunner=runner,
                           config=Config(stream=stream,
                                         plugins=DefaultPluginManager()),
                           exit=False)
        res = runner.result
        print stream.getvalue()
        self.assertEqual(res.testsRun, 0) # error is in setup
        assert not res.wasSuccessful()
        assert res.errors
        assert not res.failures

    def test_defaultTest_list(self):
        stream = StringIO()
        runner = TestRunner(stream=stream, verbosity=2)
        tests = [os.path.join(support, 'package2'),
                 os.path.join(support, 'package3')]
        prog = TestProgram(defaultTest=tests,
                           argv=['test_run_support_package2_3', '-v'],
                           testRunner=runner,
                           config=Config(),
                           exit=False)
        res = runner.result
        print stream.getvalue()
        self.assertEqual(res.testsRun, 7)

    def test_illegal_packages_not_selected(self):
        stream = StringIO()
        runner = TestRunner(stream=stream, verbosity=2)

        prog = TestProgram(defaultTest=os.path.join(support, 'issue143'),
                           argv=['test_issue_143'],
                           testRunner=runner,
                           config=Config(stream=stream,
                                         plugins=DefaultPluginManager()),
                           exit=False)
        res = runner.result
        print stream.getvalue()
        self.assertEqual(res.testsRun, 0)
        assert res.wasSuccessful()
        assert not res.errors
        assert not res.failures
        

if __name__ == '__main__':
    #import logging
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()
