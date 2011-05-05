import os
import sys
import unittest
from nose.config import Config
from nose.core import TestProgram

here = os.path.abspath(os.path.dirname(__file__))
support = os.path.join(here, 'support')
units = os.path.normpath(os.path.join(here, '..', 'unit_tests'))

if units not in sys.path:
    sys.path.insert(0, units)
from mock import RecordingPluginManager


class TestPluginCalls(unittest.TestCase):
    """
    Tests how plugins are called throughout a standard test run
    """
    def test_plugin_calls_package1(self):
        wdir = os.path.join(support, 'package1')
        man = RecordingPluginManager()
        conf = Config(plugins=man, stream=sys.stdout)
        t = TestProgram(defaultTest=wdir, config=conf,
                        argv=['test_plugin_calls_package1'], exit=False)
        print man.calls()
        assert man.called

        self.assertEqual(
            man.calls(),
            ['loadPlugins', 'addOptions', 'configure', 'begin',
             'prepareTestLoader', 'loadTestsFromNames', 'loadTestsFromName',
             'prepareTestRunner', 'prepareTest', 'setOutputStream',
             'prepareTestResult', 'beforeDirectory', 'wantFile',
             'wantDirectory', 'beforeContext', 'beforeImport',
             'afterImport', 'wantModule', 'wantClass', 'wantFunction',
             'makeTest', 'wantMethod', 'loadTestsFromTestClass',
             'loadTestsFromTestCase', 'loadTestsFromModule', 'startContext',
             'beforeTest', 'prepareTestCase', 'startTest', 'addSuccess',
             'stopTest', 'afterTest', 'stopContext', 'afterContext',
             'loadTestsFromDir', 'afterDirectory',
             'report', 'finalize'])

    def test_plugin_calls_package1_verbose(self):
        wdir = os.path.join(support, 'package1')
        man = RecordingPluginManager()
        conf = Config(plugins=man, stream=sys.stdout)
        t = TestProgram(defaultTest=wdir, config=conf,
                        argv=['test_plugin_calls_package1', '-v'], exit=False)
        print man.calls()
        assert man.called

        self.assertEqual(
            man.calls(),
            ['loadPlugins', 'addOptions', 'configure', 'begin',
             'prepareTestLoader', 'loadTestsFromNames', 'loadTestsFromName',
             'prepareTestRunner', 'prepareTest', 'setOutputStream',
             'prepareTestResult', 'beforeDirectory', 'wantFile',
             'wantDirectory', 'beforeContext', 'beforeImport',
             'afterImport', 'wantModule', 'wantClass', 'wantFunction',
             'makeTest', 'wantMethod', 'loadTestsFromTestClass',
             'loadTestsFromTestCase', 'loadTestsFromModule', 'startContext',
             'beforeTest', 'prepareTestCase', 'startTest', 'describeTest',
             'testName', 'addSuccess', 'stopTest', 'afterTest', 'stopContext',
             'afterContext', 'loadTestsFromDir', 'afterDirectory',
             'report', 'finalize'])



if __name__ == '__main__':
    unittest.main()
