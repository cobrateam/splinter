import os
import unittest
from nose.selector import Selector, TestAddress

support = os.path.abspath(os.path.join(os.path.dirname(__file__), 'support'))

class TestTestAddress(unittest.TestCase):

    def test_module_filename(self):
        wd = os.path.join(support, 'package2')
        addr = TestAddress('test_pak.test_mod', workingDir=wd)
        self.assertEqual(addr.filename,
                         os.path.join(wd, 'test_pak', 'test_mod.py'))


if __name__ == '__main__':
    unittest.main()
