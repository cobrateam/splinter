"""
Functional tests of plugin apis -- individual plugintester runs for
test plugins that implement one or more hooks for testing.
"""
import os
import sys
import unittest
from nose.plugins import Plugin, PluginTester

support = os.path.join(os.path.dirname(__file__), 'support')

class AllFail(Plugin):
    def prepareTestCase(self, test):
        self.test = test
        return self.fail

    def fail(self, result):
        result.startTest(self.test)
        try:
            try:
                assert False, "I want to fail!"
            except:
                result.addFailure(self.test, sys.exc_info())
        finally:
            result.stopTest(self.test)

class TestPrepareTestCase_MakeAllFail(PluginTester, unittest.TestCase):
    activate = '--with-allfail'
    args = ['-v']
    plugins = [AllFail()]
    suitepath = os.path.join(support, 'package2')
    
    def runTest(self):
        print "x" * 70
        print str(self.output)
        print "x" * 70
        for line in self.output:
            if line.startswith('test_pak'):
                assert line.strip().endswith('FAIL'), \
                       "Expected failure but got: %s" % line.strip()
        assert not str(self.output).strip().endswith('OK')


if __name__ == '__main__':
    unittest.main()
