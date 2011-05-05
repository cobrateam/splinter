import os
import sys
import unittest
from nose.plugins.isolate import IsolationPlugin
from nose.plugins import PluginTester

support = os.path.join(os.path.dirname(__file__), 'support')

class TestDiscovery(PluginTester, unittest.TestCase):
    activate = '--with-isolation'
    args = ['-v']
    plugins = [IsolationPlugin()]
    suitepath = os.path.join(support, 'ipt')
    
    def runTest(self):
        print str(self.output)

        for line in self.output:
            if not line.strip():
                continue
            if line.startswith('-'):
                break
            assert line.strip().endswith('ok'), \
                   "Failed test: %s" % line.strip()


class TestLoadFromNames(PluginTester, unittest.TestCase):
    activate = '--with-isolation'
    args = ['-v', 'test1/tests.py', 'test2/tests.py']
    plugins = [IsolationPlugin()]
    suitepath = None

    def setUp(self):
        self._dir = os.getcwd()
        os.chdir(os.path.join(support, 'ipt'))
        super(TestLoadFromNames, self).setUp()
        
    def tearDown(self):
        os.chdir(self._dir)
        super(TestLoadFromNames, self).tearDown()

    def makeSuite(self):
        return None
    
    def runTest(self):
        print str(self.output)

        for line in self.output:
            if not line.strip():
                continue
            if line.startswith('-'):
                break
            assert line.strip().endswith('ok'), \
                   "Failed test: %s" % line.strip()

if __name__ == '__main__':
    unittest.main()
