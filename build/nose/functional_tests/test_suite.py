import os
import sys
import unittest
from nose import case
from nose.suite import ContextSuiteFactory

support = os.path.abspath(os.path.join(os.path.dirname(__file__), 'support'))

class TestContextSuiteFactory(unittest.TestCase):

    def setUp(self):
        self._mods = sys.modules.copy()
        self._path = sys.path[:]
        sys.path.insert(0, os.path.join(support, 'package2'))

    def tearDown(self):
        to_del = [ m for m in sys.modules.keys() if
                   m not in self._mods ]
        if to_del:
            for mod in to_del:
                del sys.modules[mod]
        sys.modules.update(self._mods)
        sys.path = self._path

    def test_find_context(self):
        from test_pak import test_mod
        
        factory = ContextSuiteFactory()
        tests = [case.FunctionTestCase(test_mod.test_add),
                 case.FunctionTestCase(test_mod.test_minus)]
        suite = factory(tests)
        self.assertEqual(suite.context, test_mod)

    def test_ancestry(self):
        from test_pak.test_sub.test_mod import TestMaths
        from test_pak.test_sub import test_mod
        from test_pak import test_sub
        import test_pak
        
        factory = ContextSuiteFactory()
        ancestry = [l for l in factory.ancestry(TestMaths)]
        self.assertEqual(ancestry,
                         [test_mod, test_sub, test_pak])


if __name__ == '__main__':
    unittest.main()
