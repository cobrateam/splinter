import unittest
from nose.suite import LazySuite
from helpers import iter_compat

def gen():
    for x in range(0, 10):
        yield TestLazySuite.TC('test')

class TestLazySuite(unittest.TestCase):

    class TC(unittest.TestCase):
        def test(self):
            pass
        
    def test_basic_iteration(self):        
        ls = LazySuite(gen)
        for t in iter_compat(ls):
            assert isinstance(t, unittest.TestCase)
        
if __name__ == '__main__':
    unittest.main()
