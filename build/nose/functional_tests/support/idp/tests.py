import unittest

def test_a():
    pass

def test_b():
    raise TypeError("I am typeless")

def test_c():
    assert False, "I am contrary"

def test_gen():
    def tryit(i):
        pass
    
    for i in range(0, 4):
        yield tryit, i


class TestCase(unittest.TestCase):
    def test_a(self):
        pass
    def test_b(self):
        pass


class TestCls:
    def test_a(self):
        pass

    def test_gen(self):
        def tryit(i):
            pass
        for i in range(0, 4):
            yield tryit, i

    def test_z(self):
        pass
