import logging
import os
import re
import unittest
import nose.selector
from nose.config import Config
from nose.selector import log, Selector
from nose.util import absdir
from mock import mod

class TestSelector(unittest.TestCase):

    def tearDown(self):
        logging.getLogger('nose.selector').setLevel(logging.WARN)
    
    def test_exclude(self):
        s = Selector(Config())
        c = Config()
        c.exclude = [re.compile(r'me')]
        s2 = Selector(c)
        
        assert s.matches('test_foo')
        assert s2.matches('test_foo')
        assert s.matches('test_me')
        assert not s2.matches('test_me')
        
    def test_include(self):
        s = Selector(Config())
        c = Config()
        c.include = [re.compile(r'me')]
        s2 = Selector(c)

        assert s.matches('test')
        assert s2.matches('test')
        assert not s.matches('meatball')
        assert s2.matches('meatball')
        assert not s.matches('toyota')
        assert not s2.matches('toyota')
        
        c.include.append(re.compile('toy'))
        assert s.matches('test')
        assert s2.matches('test')
        assert not s.matches('meatball')
        assert s2.matches('meatball')
        assert not s.matches('toyota')
        assert s2.matches('toyota')
        
    def test_want_class(self):
        class Foo:
            pass
        class Bar(unittest.TestCase):
            pass
        class TestMe:
            pass
        class TestType(type):
            def __new__(cls, name, bases, dct):
                return type.__new__(cls, name, bases, dct)
        class TestClass(object):
            __metaclass__ = TestType
        
        s = Selector(Config())
        assert not s.wantClass(Foo)
        assert s.wantClass(Bar)
        assert s.wantClass(TestMe)
        assert s.wantClass(TestClass)

        TestMe.__test__ = False
        assert not s.wantClass(TestMe), "Failed to respect __test__ = False"
        Bar.__test__ = False
        assert not s.wantClass(Bar), "Failed to respect __test__ = False"
        
    def test_want_directory(self):
        s = Selector(Config())
        assert s.wantDirectory('test')
        assert not s.wantDirectory('test/whatever')
        assert s.wantDirectory('whatever/test')
        assert not s.wantDirectory('/some/path/to/unit_tests/support')

        # default src directory
        assert s.wantDirectory('lib')
        assert s.wantDirectory('src')

        # FIXME move to functional tests
        
        # this looks on disk for support/foo, which is a package
        here = os.path.abspath(os.path.dirname(__file__))
        support = os.path.join(here, 'support')
        tp = os.path.normpath(os.path.join(support, 'foo'))
        assert s.wantDirectory(tp)
        # this looks for support, which is not a package
        assert not s.wantDirectory(support)        
        
    def test_want_file(self):

        #logging.getLogger('nose.selector').setLevel(logging.DEBUG)
        #logging.basicConfig()
        
        c = Config()
        c.where = [absdir(os.path.join(os.path.dirname(__file__), 'support'))]
        base = c.where[0]
        s = Selector(c)

        assert not s.wantFile('setup.py')
        assert not s.wantFile('/some/path/to/setup.py')
        assert not s.wantFile('ez_setup.py')
        assert not s.wantFile('.test.py')
        assert not s.wantFile('_test.py')
        assert not s.wantFile('setup_something.py')
        
        assert s.wantFile('test.py')
        assert s.wantFile('foo/test_foo.py')
        assert s.wantFile('bar/baz/test.py')
        assert not s.wantFile('foo.py')
        assert not s.wantFile('test_data.txt')
        assert not s.wantFile('data.text')
        assert not s.wantFile('bar/baz/__init__.py')
        
    def test_want_function(self):
        def foo():
            pass
        def test_foo():
            pass
        def test_bar():
            pass
        
        s = Selector(Config())
        assert s.wantFunction(test_bar)
        assert s.wantFunction(test_foo)
        assert not s.wantFunction(foo)

        test_foo.__test__ = False
        assert not s.wantFunction(test_foo), \
               "Failed to respect __test__ = False"

    def test_want_method(self):
        class Baz:
            def test_me(self):
                pass
            def test_too(self):
                pass
            def other(self):
                pass
            def test_not_test(self):
                pass
            test_not_test.__test__ = False
            
        s = Selector(Config())
        
        assert s.wantMethod(Baz.test_me)
        assert s.wantMethod(Baz.test_too)
        assert not s.wantMethod(Baz.other)
        assert not s.wantMethod(Baz.test_not_test), \
               "Failed to respect __test__ = False"
        
    def test_want_module(self):
        m = mod('whatever')
        m2 = mod('this.that')
        m3 = mod('this.that.another')
        m4 = mod('this.that.another.one')
        m5 = mod('test.something')
        m6 = mod('a.test')
        m7 = mod('my_tests')
        m8 = mod('__main__')
        
        s = Selector(Config())
        assert not s.wantModule(m)
        assert not s.wantModule(m2)
        assert not s.wantModule(m3)
        assert not s.wantModule(m4)
        assert not s.wantModule(m5)
        assert s.wantModule(m6)
        assert s.wantModule(m7)
        assert s.wantModule(m8)

        m6.__test__ = False
        assert not s.wantModule(m6), "Failed to respect __test__ = False"

        
if __name__ == '__main__':
    # log.setLevel(logging.DEBUG)
    unittest.main()
