import os
import unittest
from nose.plugins.doctests import Doctest
from nose.plugins import PluginTester

support = os.path.join(os.path.dirname(__file__), 'support')

class TestDoctestPlugin(PluginTester, unittest.TestCase):
    activate = '--with-doctest'
    args = ['-v']
    plugins = [Doctest()]
    suitepath = os.path.join(support, 'dtt')
    
    def runTest(self):
        print str(self.output)
        
        assert 'Doctest: some_mod ... ok' in self.output
        assert 'Doctest: some_mod.foo ... ok' in self.output
        assert 'Ran 2 tests' in self.output
        assert str(self.output).strip().endswith('OK')


class TestDoctestFiles(PluginTester, unittest.TestCase):
    activate = '--with-doctest'
    args = ['-v', '--doctest-extension=.txt']
    plugins = [Doctest()]
    suitepath = os.path.join(support, 'dtt', 'docs')
    
    def runTest(self):
        print str(self.output)

        expect = [
            'Doctest: doc.txt ... ok',
            'Doctest: errdoc.txt ... FAIL'
            ]
        for line in self.output:
            if not line.strip():
                continue
            if line.startswith('='):
                break
            self.assertEqual(line.strip(), expect.pop(0))

if __name__ == '__main__':
    unittest.main()
