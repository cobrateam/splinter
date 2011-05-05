import logging
import os
import sys
import unittest
import nose.plugins
from optparse import OptionParser
import tempfile
from warnings import warn, filterwarnings, resetwarnings

from nose import SkipTest
from nose.pyversion import unbound_method
from nose.config import Config
from nose.plugins.attrib import AttributeSelector
from nose.plugins.base import Plugin
from nose.plugins.cover import Coverage
from nose.plugins.doctests import Doctest
from nose.plugins.prof import Profile

from mock import *

class P(Plugin):
    """Plugin of destiny!"""    
    pass

class ErrPlugin(object):
    def load(self):
        raise Exception("Failed to load the plugin")
    
class ErrPkgResources(object):
    def iter_entry_points(self, ep):
        yield ErrPlugin()

        
# some plugins have 2.4-only features
compat_24 = sys.version_info >= (2, 4)


class TestBuiltinPlugins(unittest.TestCase):

    def setUp(self):
        self.p = sys.path[:]

    def tearDown(self):
        sys.path = self.p[:]
                
    def test_add_options(self):
        conf = Config()
        opt = Bucket()
        parser = MockOptParser()
        plug = P()

        plug.add_options(parser)
        o, d = parser.opts[0]
        # print d
        assert o[0] == '--with-p'
        assert d['action'] == 'store_true'
        assert not d['default']
        assert d['dest'] == 'enable_plugin_p'
        assert d['help'] == 'Enable plugin P: Plugin of destiny! [NOSE_WITH_P]'

        opt.enable_plugin_p = True
        plug.configure(opt, conf)
        assert plug.enabled

        
class TestDoctestPlugin(unittest.TestCase):

    def setUp(self):
        self.p = sys.path[:]

    def tearDown(self):
        sys.path = self.p[:]
    
    def test_add_options(self):
        # doctest plugin adds some options...
        conf = Config()
        opt = Bucket()
        parser = MockOptParser()
        plug = Doctest()
        
        plug.add_options(parser, {})
        o, d = parser.opts[0]
        assert o[0] == '--with-doctest'

        o2, d2 = parser.opts[1]
        assert o2[0] == '--doctest-tests'
        
        o3, d3 = parser.opts[2]
        assert o3[0] == '--doctest-extension'

    def test_config(self):
        # test that configuration works properly when both environment
        # and command line specify a doctest extension
        parser = OptionParser()
        env = {'NOSE_DOCTEST_EXTENSION':'ext'}
        argv = ['--doctest-extension', 'txt']
        dtp = Doctest()
        dtp.add_options(parser, env)
        options, args = parser.parse_args(argv)
        
        print options
        print args
        self.assertEqual(options.doctestExtension, ['ext', 'txt'])

        env = {}
        parser = OptionParser()
        dtp.add_options(parser, env)
        options, args = parser.parse_args(argv)
        print options
        print args
        self.assertEqual(options.doctestExtension, ['txt'])
            
    def test_want_file(self):
        # doctest plugin can select module and/or non-module files
        conf = Config()
        opt = Bucket()
        plug = Doctest()
        plug.can_configure = True
        plug.configure(opt, conf)
        
        assert plug.wantFile('foo.py')
        assert not plug.wantFile('bar.txt')
        assert not plug.wantFile('buz.rst')
        assert not plug.wantFile('bing.mov')
        
        plug.extension = ['.txt', '.rst']
        assert plug.wantFile('/path/to/foo.py')
        assert plug.wantFile('/path/to/bar.txt')
        assert plug.wantFile('/path/to/buz.rst')
        assert not plug.wantFile('/path/to/bing.mov')
        
    def test_matches(self):
        # doctest plugin wants tests from all NON-test modules
        conf = Config()
        opt = Bucket()
        plug = Doctest()
        plug.can_configure = True
        plug.configure(opt, conf)
        assert not plug.matches('test')
        assert plug.matches('foo')

    def test_collect_pymodule(self):
        here = os.path.dirname(__file__)
        support = os.path.join(here, 'support')
        if not support in sys.path:
            sys.path.insert(0, support)
        import foo.bar.buz
        
        conf = Config()
        opt = Bucket()
        plug = Doctest()
        plug.can_configure = True
        plug.configure(opt, conf)
        suite = plug.loadTestsFromModule(foo.bar.buz)        
        expect = ['[afunc (foo.bar.buz)]']
        for test in suite:
            self.assertEqual(str(test), expect.pop(0))

    def test_addresses(self):
        here = os.path.dirname(__file__)
        support = os.path.join(here, 'support')
        if not support in sys.path:
            sys.path.insert(0, support)
        import foo.bar.buz
        
        conf = Config()
        opt = Bucket()
        plug = Doctest()
        plug.can_configure = True
        plug.configure(opt, conf)
        suite = plug.loadTestsFromModule(foo.bar.buz)
        for test in suite:
            print test.address()
            file, mod, call = test.address()
            self.assertEqual(mod, 'foo.bar.buz')
            self.assertEqual(call, None)
            for case in test:
                print case.address()
                file, mod, call = case.address()
                self.assertEqual(mod, 'foo.bar.buz')
                self.assertEqual(call, 'afunc')
            
    def test_collect_txtfile(self):
        here = os.path.abspath(os.path.dirname(__file__))
        support = os.path.join(here, 'support')
        fn = os.path.join(support, 'foo', 'doctests.txt')
        
        conf = Config()        
        opt = Bucket()
        plug = Doctest()
        plug.can_configure = True
        plug.configure(opt, conf)
        plug.extension = ['.txt']
        suite = plug.loadTestsFromFile(fn)
        for test in suite:
            assert str(test).endswith('doctests.txt')
            assert test.address(), "Test %s has no address"
        
    def test_collect_no_collect(self):
        # bug http://nose.python-hosting.com/ticket/55 
        # we got "iteration over non-sequence" when no files match
        here = os.path.abspath(os.path.dirname(__file__))
        support = os.path.join(here, 'support')
        plug = Doctest()
        for test in plug.loadTestsFromFile(os.path.join(support, 'foo')):
            self.fail("Expected no tests, got %s" % test)


class TestAttribPlugin(unittest.TestCase):

    def test_add_options(self):
        plug = AttributeSelector()
        parser = MockOptParser()
        plug.add_options(parser)

        expect = [(('-a', '--attr'),
                   {'dest': 'attr', 'action': 'append', 'default': None,
                    'metavar': 'ATTR',
                    'help': 'Run only tests that have attributes '
                    'specified by ATTR [NOSE_ATTR]'})]

        if compat_24:
            expect.append(
                (('-A', '--eval-attr'),
                 {'dest': 'eval_attr', 'action': 'append',
                  'default': None, 'metavar': 'EXPR',
                  'help': 'Run only tests for whose attributes the '
                  'Python expression EXPR evaluates to True '
                  '[NOSE_EVAL_ATTR]'}))
        self.assertEqual(parser.opts, expect)

        opt = Bucket()
        opt.attr = ['!slow']
        plug.configure(opt, Config())
        assert plug.enabled
        self.assertEqual(plug.attribs, [[('slow', False)]])

        opt.attr = ['fast,quick', 'weird=66']
        plug.configure(opt, Config())
        self.assertEqual(plug.attribs, [[('fast', True),
                                         ('quick', True)],
                                        [('weird', '66')]])

        # don't die on trailing ,
        opt.attr = [ 'something,' ]
        plug.configure(opt, Config())
        self.assertEqual(plug.attribs, [[('something', True)]] )
        
        if compat_24:
            opt.attr = None
            opt.eval_attr = [ 'weird >= 66' ]
            plug.configure(opt, Config())
            self.assertEqual(plug.attribs[0][0][0], 'weird >= 66')
            assert callable(plug.attribs[0][0][1])
                       
    def test_basic_attr(self):
        def f():
            pass
        f.a = 1

        def g():
            pass
    
        plug = AttributeSelector()
        plug.attribs = [[('a', True)]]
        assert plug.wantFunction(f) is not False
        assert not plug.wantFunction(g)

    def test_class_attr(self):
        class TestP:
            foo = True
            def h():
                pass

        def i():
            pass
        
        plug = AttributeSelector()
        plug.attribs = [[('foo', True)]]
        assert plug.wantMethod(unbound_method(TestP, TestP.h)) is not False
        assert plug.wantFunction(i) is False
        
    def test_eval_attr(self):
        if not compat_24:
            warn("No support for eval attributes in python versions older"
                 " than 2.4")
            return
        def f():
            pass
        f.monkey = 2
        
        def g():
            pass
        g.monkey = 6

        def h():
            pass
        h.monkey = 5
        
        cnf = Config()
        opt = Bucket()
        opt.eval_attr = "monkey > 5"
        plug = AttributeSelector()
        plug.configure(opt, cnf)

        assert not plug.wantFunction(f)
        assert plug.wantFunction(g) is not False
        assert not plug.wantFunction(h)

    def test_attr_a_b(self):
        def f1():
            pass
        f1.tags = ['a', 'b']

        def f2():
            pass
        f2.tags = ['a', 'c']

        def f3():
            pass
        f3.tags = ['b', 'c']

        def f4():
            pass
        f4.tags = ['c', 'd']
        
        cnf = Config()
        parser = OptionParser()
        plug = AttributeSelector()

        plug.add_options(parser)

        # OR
        opt, args = parser.parse_args(['test', '-a', 'tags=a',
                                       '-a', 'tags=b'])
        print opt
        plug.configure(opt, cnf)

        assert plug.wantFunction(f1) is None
        assert plug.wantFunction(f2) is None
        assert plug.wantFunction(f3) is None
        assert not plug.wantFunction(f4)

        # AND
        opt, args = parser.parse_args(['test', '-a', 'tags=a,tags=b'])
        print opt
        plug.configure(opt, cnf)

        assert plug.wantFunction(f1) is None
        assert not plug.wantFunction(f2)
        assert not plug.wantFunction(f3)
        assert not plug.wantFunction(f4)
        

class TestProfPlugin(unittest.TestCase):

    def setUp(self):        
        if not Profile.available():
            raise SkipTest('profile plugin not available; skipping')

    def test_options(self):
        parser = OptionParser()
        conf = Config()
        plug = Profile()

        plug.add_options(parser, {})
        opts = [ o._long_opts[0] for o in parser.option_list ]
        assert '--profile-sort' in opts
        assert '--profile-stats-file' in opts
        assert '--with-profile' in opts
        assert '--profile-restrict' in opts

    def test_begin(self):
        plug = Profile()
        plug.pfile = tempfile.mkstemp()[1]
        try:
            plug.begin()
            assert plug.prof
        finally:
            plug.finalize(None)

    def test_prepare_test(self):
        r = {}
        class dummy:
            def runcall(self, f, r):
                r[1] = f(), "wrapped"
        def func():
            return "func"
        
        plug = Profile()
        plug.prof = dummy()
        result = plug.prepareTest(func)
        try:
            result(r)
            assert r[1] == ("func", "wrapped")
        finally:
            plug.finalize(None)

    def test_finalize(self):
        def func():
            pass

        plug = Profile()
        plug.begin()
        plug.prepareTest(func)
        pfile = plug.pfile
        try:
            assert os.path.exists(pfile)
        finally:
            plug.finalize(None)
        assert not os.path.exists(pfile), \
               "finalize did not remove temp file %s" % pfile

if __name__ == '__main__':
    unittest.main()
