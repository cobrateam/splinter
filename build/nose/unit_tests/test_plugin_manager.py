import unittest
from nose import case
from nose.plugins import Plugin, PluginManager


class Plug(Plugin):
    def loadTestsFromFile(self, path):
        class TC(unittest.TestCase):
            def test(self):
                pass
        return [TC('test')]
    def addError(self, test, err):
        return True

class Plug2(Plugin):
    def loadTestsFromFile(self, path):
        class TCT(unittest.TestCase):
            def test_2(self):
                pass
        return [TCT('test_2')]
    def addError(self, test, err):
        assert False, "Should not have been called"

class Plug3(Plugin):
    def loadTestsFromModule(self, module):
        raise TypeError("I don't like to type")

class Plug4(Plugin):
    def loadTestsFromModule(self, module):
        raise AttributeError("I am missing my nose")

class BetterPlug2(Plugin):
    name = 'plug2'


class TestPluginManager(unittest.TestCase):

    def test_proxy_to_plugins(self):
        man = PluginManager(plugins=[Plug(), Plug2()])

        # simple proxy: first plugin to return a value wins
        self.assertEqual(man.addError(None, None), True)

        # multiple proxy: all plugins that return values get to run
        all = []
        for res in man.loadTestsFromFile('foo'):
            print res
            all.append(res)
        self.assertEqual(len(all), 2)

    def test_iter(self):
        expect = [Plug(), Plug2()]
        man = PluginManager(plugins=expect)
        for plug in man:
            self.assertEqual(plug, expect.pop(0))
        assert not expect, \
               "Some plugins were not found by iteration: %s" % expect

    def test_plugin_generative_method_errors_not_hidden(self):
        import nose.failure
        pm = PluginManager(plugins=[Plug3(), Plug4()])
        loaded = list(pm.loadTestsFromModule('whatever'))
        self.assertEqual(len(loaded), 2)
        for test in loaded:
            assert isinstance(test, nose.failure.Failure), \
            "%s is not a failure" % test

    def test_plugin_override(self):
        pm = PluginManager(plugins=[Plug2(), BetterPlug2()])
        self.assertEqual(len(pm.plugins), 1)
        assert isinstance(pm.plugins[0], BetterPlug2)

if __name__ == '__main__':
    unittest.main()
