import os
import sys
import unittest

from nose.plugins import PluginTester
from nose.plugins.builtin import FailureDetail, Capture

support = os.path.join(os.path.dirname(__file__), 'support')


class TestFailureDetailWorks(PluginTester, unittest.TestCase):
    activate = '-d'
    plugins = [FailureDetail()]
    args = ['-v']
    suitepath = os.path.join(support, 'issue072')

    def test_assert_info_in_output(self):
        print
        print '!' * 70
        print str(self.output)
        print '!' * 70
        print
        assert '>>  assert 4 == 2' in str(self.output)

class TestFailureDetailWorksWhenChained(PluginTester, unittest.TestCase):
    activate = '-d'
    plugins = [FailureDetail(), Capture()]
    args = ['-v']
    suitepath = os.path.join(support, 'issue072')

    def test_assert_info_and_capt_stdout_in_output(self):
        out = str(self.output)
        print
        print 'x' * 70
        print out
        print 'x' * 70
        print
        
        assert '>>  assert 4 == 2' in out, \
               "Assert info not found in chained output"
        assert 'something' in out, \
               "Captured stdout not found in chained output"
        
if __name__ == '__main__':
    unittest.main()
