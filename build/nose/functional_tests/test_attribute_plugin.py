import os
import sys
import unittest
from nose.plugins.attrib import AttributeSelector
from nose.plugins import PluginTester

support = os.path.join(os.path.dirname(__file__), 'support')

compat_24 = sys.version_info >= (2, 4)

class TestSimpleAttribute(PluginTester, unittest.TestCase):
    activate = "-a a"
    args = ['-v']
    plugins = [AttributeSelector()]
    suitepath = os.path.join(support, 'att')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70
        
        assert 'test_attr.test_one ... ok' in self.output
        assert 'test_attr.test_two ... ok' in self.output
        assert 'TestClass.test_class_one ... ok' in self.output
        assert 'TestClass.test_class_two ... ok' in self.output
        assert 'TestClass.test_class_three ... ok' in self.output
        assert 'test_three' not in self.output
        assert 'test_case_two' not in self.output
        assert 'test_case_one' not in self.output
        assert 'test_case_three' not in self.output


class TestNotSimpleAttribute(PluginTester, unittest.TestCase):
    activate = "-a !a"
    args = ['-v']
    plugins = [AttributeSelector()]
    suitepath = os.path.join(support, 'att')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70
        
        assert 'test_attr.test_one ... ok' not in self.output
        assert 'test_attr.test_two ... ok' not in self.output
        assert 'TestClass.test_class_one ... ok' not in self.output
        assert 'TestClass.test_class_two ... ok' not in self.output
        assert 'TestClass.test_class_three ... ok' not in self.output
        assert 'test_three' in self.output
        assert 'test_case_two' in self.output
        assert 'test_case_one' in self.output
        assert 'test_case_three' in self.output


class TestAttributeValue(PluginTester, unittest.TestCase):
    activate = "-a b=2"
    args = ['-v']
    plugins = [AttributeSelector()]
    suitepath = os.path.join(support, 'att')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70
        
        assert 'test_attr.test_one ... ok' not in self.output
        assert 'test_attr.test_two ... ok' not in self.output
        assert 'test_attr.test_three ... ok' not in self.output
        assert 'TestClass.test_class_one ... ok' not in self.output
        assert 'TestClass.test_class_two ... ok' in self.output
        assert 'TestClass.test_class_three ... ok' not in self.output
        assert 'test_case_two' in self.output
        assert 'test_case_one' in self.output
        assert 'test_case_three' in self.output


class TestAttributeArray(PluginTester, unittest.TestCase):
    activate = "-a d=2"
    args = ['-v']
    plugins = [AttributeSelector()]
    suitepath = os.path.join(support, 'att')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70
        
        assert 'test_attr.test_one ... ok' in self.output
        assert 'test_attr.test_two ... ok' in self.output
        assert 'test_attr.test_three ... ok' not in self.output
        assert 'TestClass.test_class_one ... ok' not in self.output
        assert 'TestClass.test_class_two ... ok' not in self.output
        assert 'TestClass.test_class_three ... ok' not in self.output
        assert 'test_case_two' not in self.output
        assert 'test_case_one' not in self.output
        assert 'test_case_three' not in self.output


class TestAttributeArrayAnd(PluginTester, unittest.TestCase):
    activate = "-a d=1,d=2"
    args = ['-v']
    plugins = [AttributeSelector()]
    suitepath = os.path.join(support, 'att')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70
        
        assert 'test_attr.test_one ... ok' in self.output
        assert 'test_attr.test_two ... ok' not in self.output
        assert 'test_attr.test_three ... ok' not in self.output
        assert 'TestClass.test_class_one ... ok' not in self.output
        assert 'TestClass.test_class_two ... ok' not in self.output
        assert 'TestClass.test_class_three ... ok' not in self.output
        assert 'test_case_two' not in self.output
        assert 'test_case_one' not in self.output
        assert 'test_case_three' not in self.output


class TestAttributeArrayOr(PluginTester, unittest.TestCase):
    activate = "-v"
    args = ['-a', 'd=1', '-a', 'd=2']
    plugins = [AttributeSelector()]
    suitepath = os.path.join(support, 'att')

    def runTest(self):
        print '*' * 70
        print str(self.output)
        print '*' * 70
        
        assert 'test_attr.test_one ... ok' in self.output
        assert 'test_attr.test_two ... ok' in self.output
        assert 'test_attr.test_three ... ok' in self.output
        assert 'TestClass.test_class_one ... ok' not in self.output
        assert 'TestClass.test_class_two ... ok' not in self.output
        assert 'TestClass.test_class_three ... ok' not in self.output
        assert 'test_case_two' not in self.output
        assert 'test_case_one' not in self.output
        assert 'test_case_three' not in self.output
        

if compat_24:
    class TestAttributeEval(PluginTester, unittest.TestCase):
        activate = "-A c>20"
        args = ['-v']
        plugins = [AttributeSelector()]
        suitepath = os.path.join(support, 'att')

        def runTest(self):
            print '*' * 70
            print str(self.output)
            print '*' * 70

            assert 'test_attr.test_one ... ok' not in self.output
            assert 'test_attr.test_two ... ok' not in self.output
            assert 'test_attr.test_three ... ok' not in self.output
            assert 'TestClass.test_class_one ... ok' not in self.output
            assert 'TestClass.test_class_two ... ok' not in self.output
            assert 'TestClass.test_class_three ... ok' not in self.output
            assert 'test_case_two' in self.output
            assert 'test_case_one' not in self.output
            assert 'test_case_three' not in self.output

if __name__ == '__main__':
    #import logging
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()
