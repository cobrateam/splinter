import os
import sys
import unittest
from cStringIO import StringIO
from nose.core import TestProgram
from test_program import TestRunner

here = os.path.dirname(__file__)
support = os.path.join(here, 'support')

class TestNamespacePackages(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()
        self.orig_path = sys.path[:]
        test_dir = os.path.join(support, 'namespace_pkg')
        os.chdir(test_dir)
        sys.path.append(os.path.join(test_dir, 'site-packages'))

    def tearDown(self):
        sys.path = self.orig_path
        os.chdir(self.cwd)

    def test_namespace_pkg(self):
        """Ensure namespace packages work/can import from each other"""
        stream = StringIO()
        runner = TestRunner(stream=stream)
        runner.verbosity = 2
        prog = TestProgram(argv=[''],
                           testRunner=runner,
                           exit=False)
        res = runner.result
        self.assertEqual(res.testsRun, 1,
                         "Expected to run 1 test, ran %s" % res.testsRun)
        assert res.wasSuccessful()
        assert not res.errors
        assert not res.failures

    def test_traverse_namespace(self):
        """Ensure the --traverse-namespace option tests the other
        namespace package sibling also.
        """
        stream = StringIO()
        runner = TestRunner(stream=stream)
        runner.verbosity = 2
        prog = TestProgram(argv=['', '--traverse-namespace'],
                           testRunner=runner,
                           exit=False)
        res = runner.result
        self.assertEqual(res.testsRun, 2,
                         "Expected to run 2 tests, ran %s" % res.testsRun)
        assert res.wasSuccessful()
        assert not res.errors
        assert not res.failures


if __name__ == '__main__':
    unittest.main()
