import os
import unittest
from nose.plugins.plugintest import PluginTester, remove_timings

support = os.path.join(os.path.dirname(__file__), 'support')


class TestSingleTestPass(PluginTester, unittest.TestCase):
    activate = '-v'
    plugins = []
    suitepath = os.path.join(support, 'pass')

    def test_single_test_pass(self):
        # note that this doesn't use nose.plugins.doctests.run, in order that
        # this test fails if the final terminating newline is not present (it
        # could still be written as a doctest -- PluginTester was just closer
        # to hand)
        print self.output
        output = remove_timings(str(self.output))
        assert output == """\
test.test ... ok

----------------------------------------------------------------------
Ran 1 test in ...s

OK
"""

class TestZeroTestsPass(PluginTester, unittest.TestCase):
    activate = '-v'
    plugins = []
    suitepath = os.path.join(support, 'empty')

    def test_zero_tests_pass(self):
        print self.output
        output = remove_timings(str(self.output))
        assert output == """\

----------------------------------------------------------------------
Ran 0 tests in ...s

OK
"""
