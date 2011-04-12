import unittest
import nose.selector
from nose.config import Config
from nose.plugins.base import Plugin
from nose.plugins.manager import PluginManager

class TestSelectorPlugins(unittest.TestCase):

    def test_rejection(self):
        class EvilSelector(Plugin):
            def wantFile(self, filename, package=None):
                if 'good' in filename:
                    return False
                return None

        c = Config(plugins=PluginManager(plugins=[EvilSelector()]))
        s = nose.selector.Selector(c)
        s2 = nose.selector.Selector(Config())
        
        assert s.wantFile('test_neutral.py')
        assert s2.wantFile('test_neutral.py')
        
        assert s.wantFile('test_evil.py')
        assert s2.wantFile('test_evil.py')
        
        assert not s.wantFile('test_good.py')
        assert s2.wantFile('test_good.py')
        
if __name__ == '__main__':
    unittest.main()
