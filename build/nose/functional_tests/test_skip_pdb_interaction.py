import unittest
from nose import case
from nose.config import Config
from nose.plugins import debug
from nose.plugins.manager import PluginManager
from nose.plugins.skip import Skip, SkipTest
from nose.proxy import ResultProxyFactory


class StubPdb:
    called = False
    def post_mortem(self, tb):
        self.called = True

class TestSkipPdbInteraction(unittest.TestCase):
    """Tests interaction between skip plugin and pdb plugin -- pdb should
    not fire on a skip error
    """
    def setUp(self):
        self._pdb = debug.pdb
        debug.pdb = StubPdb()

    def tearDown(self):
        debug.pdb = self._pdb
    
    def test_skip_prevents_pdb_call(self):

        class TC(unittest.TestCase):
            def test(self):
                raise SkipTest('not me')

        skip = Skip()
        skip.enabled = True
        p = debug.Pdb()
        p.enabled = True
        p.enabled_for_errors = True
        res = unittest.TestResult()
        conf = Config(plugins=PluginManager(plugins=[skip, p]))        
        rpf = ResultProxyFactory(conf)
        test = case.Test(TC('test'), resultProxy=rpf)
        test(res)

        assert not res.errors, "Skip was recorded as error %s" % res.errors
        assert not debug.pdb.called, "pdb was called"

        

if __name__ == '__main__':
    unittest.main()
