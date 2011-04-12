import os
import sys
import unittest
import warnings
from cStringIO import StringIO
from nose.result import _TextTestResult
here = os.path.dirname(__file__)
support = os.path.join(here, 'support')


class TestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        self.result = _TextTestResult(
            self.stream, self.descriptions, self.verbosity)
        return self.result


class TestNoseTestCollector(unittest.TestCase):

    def test_skip_works_with_collector(self):
        verbosity = 2
        stream = StringIO()
        runner = TestRunner(stream=stream, verbosity=verbosity)
        pwd = os.getcwd()

        # we don't need to see our own warnings
        warnings.filterwarnings(action='ignore',
                                category=RuntimeWarning,
                                module='nose.plugins.manager')

        try:
            os.chdir(os.path.join(support, 'issue038'))
            unittest.TestProgram(
                None, None,
                argv=['test_collector', '-v', 'nose.collector'],
                testRunner=runner)
        except SystemExit:
            pass
        os.chdir(pwd)
        out = stream.getvalue()
        assert runner.result.wasSuccessful()
        assert 'SKIP' in out, "SKIP not found in %s" % out


if __name__ == '__main__':
    unittest.main()
