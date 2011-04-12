"""
Tests that plugins can override loadTestsFromTestCase
"""
import os
import unittest
from nose import loader
from nose.plugins import PluginTester
from nose.plugins.base import Plugin


support = os.path.join(os.path.dirname(__file__), 'support')


class NoFixturePlug(Plugin):
    enabled = True

    def options(self, parser, env):
        print "options"        
        pass
    
    def configure(self, options, conf):
        print "configure"
        pass

    def loadTestsFromTestCase(self, testCaseClass):
        print "Called!"
        class Derived(testCaseClass):
            def setUp(self):
                pass
            def tearDown(self):
                pass
        # must use nose loader here because the default loader in 2.3
        # won't load tests from base classes
        l = loader.TestLoader()
        return l.loadTestsFromTestCase(Derived)


class TestLoadTestsFromTestCaseHook(PluginTester, unittest.TestCase):

    activate = '-v'
    args = []
    plugins = [NoFixturePlug()]
    suitepath = os.path.join(support, 'ltftc')

    def runTest(self):
        expect = [
            'test_value (%s.Derived) ... ERROR' % __name__,
            'test_value (tests.Tests) ... ok']
        print str(self.output)
        for line in self.output:
            if expect:
                self.assertEqual(line.strip(), expect.pop(0))
                

if __name__ == '__main__':
    unittest.main()
