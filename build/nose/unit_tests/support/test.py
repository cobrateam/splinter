import unittest

class Something(unittest.TestCase):
    def test_something(self):
        pass

class TestTwo:

    def __repr__(self):
        return 'TestTwo'
    
    def test_whatever(self):
        pass
