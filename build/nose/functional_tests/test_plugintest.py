
import unittest, os
from nose.plugins import PluginTester, Plugin
from nose.tools import eq_
from cStringIO import StringIO

class StubPlugin(Plugin):
    def options(self, parser, env=os.environ):
        super(StubPlugin, self).options(parser, env=env)
    def configure(self, options, conf):
        pass    

class SomePluginTestCase(PluginTester):
    activate = None # set this to --with-yourplugin, etc
    plugins = [] # list of plugin instances
    
    def makeSuite(self):
        class SomeTest(unittest.TestCase):
            def runTest(self):
                raise ValueError("Now do something, plugin!")
        return unittest.TestSuite([SomeTest()])      

class TestPluginTester(unittest.TestCase):
    def _runPluginTest(self, test_case):
        loader = unittest.TestLoader()
        suite = loader.loadTestsFromTestCase(test_case)
        res = unittest.TestResult()
        suite(res)
        return res
        
    def testPluginTesterExecsPlugin(self):
        called = []
        class MockExecPlugin(StubPlugin):
            def configure(self, options, conf):
                called.append('configure')
        
        class MockExecTestCase(SomePluginTestCase, unittest.TestCase):
            activate = '--with-mockexec'
            plugins = [MockExecPlugin()]
            
            def test_something_anything(self):
                # here is where the test case would test
                # that the plugin interacted with stub tests
                pass      
            
        res = self._runPluginTest(MockExecTestCase)
        eq_(res.testsRun, 1)
        eq_(called[0], 'configure')

if __name__ == '__main__':
    unittest.main()