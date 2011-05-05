import os
import unittest
import nose
from nose import case
from nose.pyversion import unbound_method
# don't import * -- some util functions look testlike
from nose import util

np = os.path.normpath

class TestUtils(unittest.TestCase):
    
    def test_file_like(self):
        file_like = util.file_like
        assert file_like('a/file')
        assert file_like('file.py')
        assert file_like('/some/file.py')
        assert not file_like('a.file')
        assert not file_like('some.package')
        assert file_like('a-file')
        assert not file_like('test')
        
    def test_split_test_name(self):
        split_test_name = util.split_test_name
        assert split_test_name('a.package:Some.method') == \
            (None, 'a.package', 'Some.method')
        assert split_test_name('some.module') == \
            (None, 'some.module', None)
        assert split_test_name('this/file.py:func') == \
            (np('this/file.py'), None, 'func')
        assert split_test_name('some/file.py') == \
            (np('some/file.py'), None, None)
        assert split_test_name(':Baz') == \
            (None, None, 'Baz')
        assert split_test_name('foo:bar/baz.py') == \
            (np('foo:bar/baz.py'), None, None)

    def test_split_test_name_windows(self):
        # convenience
        stn = util.split_test_name
        self.assertEqual(stn(r'c:\some\path.py:a_test'),
                         (np(r'c:\some\path.py'), None, 'a_test'))
        self.assertEqual(stn(r'c:\some\path.py'),
                         (np(r'c:\some\path.py'), None, None))
        self.assertEqual(stn(r'c:/some/other/path.py'),
                         (np(r'c:/some/other/path.py'), None, None))
        self.assertEqual(stn(r'c:/some/other/path.py:Class.test'),
                         (np(r'c:/some/other/path.py'), None, 'Class.test'))
        try:
            stn('cat:dog:something')
        except ValueError:
            pass
        else:
            self.fail("Nonsense test name should throw ValueError")

    def test_test_address(self):
        # test addresses are specified as
        #     package.module:class.method
        #     /path/to/file.py:class.method
        # converted into 3-tuples (file, module, callable)
        # all terms optional
        test_address = util.test_address
        absfile = util.absfile
        class Foo:
            def bar(self):
                pass
        def baz():
            pass

        f = Foo()

        class FooTC(unittest.TestCase):
            def test_one(self):
                pass
            def test_two(self):
                pass

        class CustomTestType(type):
            pass
        class CustomTC(unittest.TestCase):
            __metaclass__ = CustomTestType
            def test_one(self):
                pass
            def test_two(self):
                pass

        foo_funct = case.FunctionTestCase(baz)
        foo_functu = unittest.FunctionTestCase(baz)

        foo_mtc = case.MethodTestCase(unbound_method(Foo, Foo.bar))

        me = util.src(absfile(__file__))
        self.assertEqual(test_address(baz),
                         (me, __name__, 'baz'))
        assert test_address(Foo) == (me, __name__, 'Foo')
        assert test_address(unbound_method(Foo, Foo.bar)) == (me, __name__,
                                                              'Foo.bar')
        assert test_address(f) == (me, __name__, 'Foo')
        assert test_address(f.bar) == (me, __name__, 'Foo.bar')
        assert test_address(nose) == (
            util.src(absfile(nose.__file__)), 'nose', None)

        # test passing the actual test callable, as the
        # missed test plugin must do
        self.assertEqual(test_address(FooTC('test_one')),
                         (me, __name__, 'FooTC.test_one'))
        self.assertEqual(test_address(CustomTC('test_one')),
                         (me, __name__, 'CustomTC.test_one'))
        self.assertEqual(test_address(foo_funct),
                         (me, __name__, 'baz'))
        self.assertEqual(test_address(foo_functu),
                         (me, __name__, 'baz'))
        self.assertEqual(test_address(foo_mtc),
                         (me, __name__, 'Foo.bar'))

    def test_isclass_detects_classes(self):
        class TC(unittest.TestCase):
            pass
        class TC_Classic:
            pass
        class TC_object(object):
            pass
        # issue153 -- was not detecting custom typed classes...
        class TCType(type):
            pass
        class TC_custom_type(object):
            __metaclass__ = TCType
        class TC_unittest_custom_type(unittest.TestCase):
            __metaclass__ = TCType
        
        assert util.isclass(TC), "failed to detect %s as class" % TC
        assert util.isclass(TC_Classic), "failed to detect %s as class" % TC_Classic
        assert util.isclass(TC_object), "failed to detect %s as class" % TC_object
        assert util.isclass(TC_custom_type), "failed to detect %s as class" % TC_custom_type
        assert util.isclass(TC_unittest_custom_type), "failed to detect %s as class" % TC_unittest_custom_type
        
    def test_isclass_ignores_nonclass_things(self):
        anint = 1
        adict = {}
        assert not util.isclass(anint), "should have ignored %s" % type(anint)
        assert not util.isclass(adict), "should have ignored %s" % type(adict)

    def test_tolist(self):
        tolist = util.tolist
        assert tolist('foo') == ['foo']
        assert tolist(['foo', 'bar']) == ['foo', 'bar']
        assert tolist('foo,bar') == ['foo', 'bar']
        self.assertEqual(tolist('.*foo/.*,.1'), ['.*foo/.*', '.1'])

    def test_try_run(self):
        try_run = util.try_run
        import imp

        def bar():
            pass

        def bar_m(mod):
            pass

        class Bar:
            def __call__(self):
                pass

        class Bar_m:
            def __call__(self, mod):
                pass
        
        foo = imp.new_module('foo')
        foo.bar = bar
        foo.bar_m = bar_m
        foo.i_bar = Bar()
        foo.i_bar_m = Bar_m()

        try_run(foo, ('bar',))
        try_run(foo, ('bar_m',))
        try_run(foo, ('i_bar',))
        try_run(foo, ('i_bar_m',))
        
if __name__ == '__main__':
    unittest.main()
