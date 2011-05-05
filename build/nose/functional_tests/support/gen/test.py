"""This test will fail if generators bind too early."""
    
from nose.tools import eq_

def test1():

    def func(_l, _n):
        eq_(len(_l), _n)
    l = []
    for i in xrange(5):
        yield func, l, i
        l.append(None)
