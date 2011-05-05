import os
import sys
import unittest
from nose.plugins.failuredetail import FailureDetail
from nose.plugins.capture import Capture
from nose.plugins import PluginTester

support = os.path.join(os.path.dirname(__file__), 'support')

class TestFailureDetail(PluginTester, unittest.TestCase):
    activate = "-d"
    args = ['-v']
    plugins = [FailureDetail()]
    suitepath = os.path.join(support, 'fdp')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70

        expect = \
        'AssertionError: a is not 4\n'
        '    print "Hello"\n'
        '    2 = 2\n'
        '>>  assert 2 == 4, "a is not 4"'

        assert expect in self.output


class TestFailureDetailWithCapture(PluginTester, unittest.TestCase):
    activate = "-d"
    args = ['-v']
    plugins = [FailureDetail(), Capture()]
    suitepath = os.path.join(support, 'fdp/test_fdp_no_capt.py')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70

        expect = \
        'AssertionError: a is not 4\n'
        '    print "Hello"\n'
        '    2 = 2\n'
        '>>  assert 2 == 4, "a is not 4"'

        assert expect in self.output

if __name__ == '__main__':
    unittest.main()
