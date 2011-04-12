
from nose.tools import eq_
from nose.plugins.attrib import attr

def test_flags():
    # @attr('one','two')
    def test():
        pass
    test = attr('one','two')(test)
    
    eq_(test.one, 1)
    eq_(test.two, 1)

def test_values():
    # @attr(mood="hohum", colors=['red','blue'])
    def test():
        pass
    test = attr(mood="hohum", colors=['red','blue'])(test)
    
    eq_(test.mood, "hohum")
    eq_(test.colors, ['red','blue'])

def test_mixed():
    # @attr('slow', 'net', role='integration')
    def test():
        pass
    test = attr('slow', 'net', role='integration')(test)
    
    eq_(test.slow, 1)
    eq_(test.net, 1)
    eq_(test.role, 'integration')
    