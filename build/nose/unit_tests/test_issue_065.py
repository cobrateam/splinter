import os
from nose import loader
import unittest

support = os.path.join(os.path.dirname(__file__), 'support')

class TestIssue065(unittest.TestCase):
    def test_dict_wrapper_instance_not_loaded(self):
        wd = os.path.join(support, 'issue065')
        l = loader.TestLoader() #workingDir=wd)
        tests = l.loadTestsFromDir(wd)
        tests = list(tests)
        self.assertEqual(len(tests), 1)
        tests = list(tests[0])
        assert not tests, "Tests were loaded from module with no tests"
        


if __name__ == '__main__':
    unittest.main()
