import imp
import os
import sys
import unittest
from nose.loader import TestLoader as Loader

from nose import util, loader, selector # so we can set mocks
import nose.case


def safepath(p):
    """Helper function to make cross-platform safe paths
    """
    return p.replace('/', os.sep)


def mods():
    #
    # Setting up the fake modules that we'll use for testing
    # test loading
    #
    M = {}
    M['test_module'] = imp.new_module('test_module')
    M['module'] = imp.new_module('module')
    M['package'] = imp.new_module('package')
    M['package'].__path__ = [safepath('/package')]
    M['package'].__file__ = safepath('/package/__init__.py')
    M['package.subpackage'] = imp.new_module('package.subpackage')
    M['package'].subpackage = M['package.subpackage']
    M['package.subpackage'].__path__ = [safepath('/package/subpackage')]
    M['package.subpackage'].__file__ = safepath(
        '/package/subpackage/__init__.py')
    M['test_module_with_generators'] = imp.new_module(
        'test_module_with_generators')
    M['test_module_with_metaclass_tests'] = imp.new_module(
        'test_module_with_metaclass_tests')

    # a unittest testcase subclass
    class TC(unittest.TestCase):
        def runTest(self):
            pass

    class TC2(unittest.TestCase):
        def runTest(self):
            pass
    
    # test class that uses a metaclass
    class TCType(type):
        def __new__(cls, name, bases, dct):
            return type.__new__(cls, name, bases, dct)
    class TestMetaclassed(object):
        __metaclass__ = TCType
        def test_one(self):
            pass
        def test_two(self):
            pass

    # test function
    def test_func():
        pass

    # non-testcase-subclass test class
    class TestClass:

        def test_func(self):
            pass

        def test_generator_inline(self):
            """docstring for test generator inline
            """
            def test_odd(v):
                assert v % 2
            for i in range(0, 4):
                yield test_odd, i

        def test_generator_method(self):
            """docstring for test generator method
            """
            for i in range(0, 4):
                yield self.try_odd, i

        def test_generator_method_name(self):
            """docstring for test generator method name
            """
            for i in range(0, 4):
                yield 'try_odd', i

        def try_odd(self, v):
            assert v % 2

    # test function that is generator
    def test_func_generator():
        """docstring for test func generator
        """
        def test_odd(v):
            assert v % 2
        for i in range(0, 4):
            yield test_odd, i

    def test_func_generator_name():
        """docstring for test func generator name
        """
        for i in range(0, 4):
            yield 'try_odd', i

    def try_odd(v):
        assert v % 2

    M['nose'] = nose
    M['__main__'] = sys.modules['__main__']
    M['test_module'].TC = TC
    TC.__module__ = 'test_module'
    M['test_module'].test_func = test_func
    test_func.__module__ = 'test_module'
    M['module'].TC2 = TC2
    TC2.__module__ = 'module'
    M['test_module_with_generators'].TestClass = TestClass
    TestClass.__module__ = 'test_module_with_generators'
    M['test_module_with_generators'].test_func_generator = test_func_generator
    M['test_module_with_generators'].test_func_generator_name = \
        test_func_generator_name
    M['test_module_with_generators'].try_odd = try_odd
    test_func_generator_name.__module__ = 'test_module_with_generators'
    test_func_generator.__module__ = 'test_module_with_generators'
    try_odd.__module__ = 'test_module_with_generators'
    M['test_module_with_metaclass_tests'].TestMetaclassed = TestMetaclassed
    TestMetaclassed.__module__ = 'test_module_with_metaclass_tests'
    del TC
    del TC2
    del TestMetaclassed
    # del TCType
    del test_func
    del TestClass
    del test_func_generator
    return M

M = mods()

# Mock the filesystem access so we don't have to maintain
# a support dir with real files
_listdir = os.listdir
_isdir = os.path.isdir
_isfile = os.path.isfile
_exists = os.path.exists
_import = __import__


#
# Mock functions
#
def mock_listdir(path):
    if path.endswith(safepath('/package')):
        return ['.', '..', 'subpackage', '__init__.py']
    elif path.endswith(safepath('/subpackage')):
        return ['.', '..', '__init__.py']
    elif path.endswith(safepath('/sort')):
        return ['.', '..', 'lib', 'src', 'test', 'test_module.py', 'a_test']
    return ['.', '..', 'test_module.py', 'module.py']


def mock_isdir(path):
    print "is dir '%s'?" % path
    paths = map(safepath, [
        '/a/dir/path', '/package',
        '/package/subpackage', '/sort/lib',
        '/sort/src', '/sort/a_test',
        '/sort/test', '/sort'])
    paths = paths + map(os.path.abspath, paths)
    if path in paths:
        return True
    return False


def mock_isfile(path):
    if path in ('.', '..'):
        return False
    return '.' in path


def mock_exists(path):
    print "exists '%s'?" % path
    paths = map(safepath, [
        '/package', '/package/__init__.py', '/package/subpackage',
        '/package/subpackage/__init__.py'
        ])
    paths = paths + map(os.path.abspath, paths)
    return path in paths


def mock_import(modname, gl=None, lc=None, fr=None):
    if gl is None:
        gl = M
    if lc is None:
        lc = locals()
    try:
        mod = sys.modules[modname]
    except KeyError:
        pass
    try:
        pname = []
        for part in modname.split('.'):
            pname.append(part)
            mname = '.'.join(pname)
            mod = gl[mname]
            sys.modules[mname] = mod
        return mod
    except KeyError:
        raise ImportError("No '%s' in fake module list" % modname)    


class MockImporter:
    def importFromPath(self, path, fqname):
        try:
            m = M[fqname]
        except KeyError:
            raise ImportError(fqname)
        sys.modules[fqname] = m
        return m
    
#
# Tests
#
class TestTestLoader(unittest.TestCase):

    def setUp(self):
        os.listdir = mock_listdir
        loader.op_isdir = selector.op_isdir = os.path.isdir = mock_isdir
        loader.op_isfile = selector.op_isfile = os.path.isfile = mock_isfile
        selector.op_exists = os.path.exists = mock_exists
        util.__import__ = mock_import
        self.l = Loader(importer=MockImporter())#, context=MockContext)

    def tearDown(self):
        os.listdir = _listdir
        loader.op_isdir = selector.op_isdir = os.path.isdir = _isdir
        loader.op_isfile = selector.op_isfile = os.path.isfile = _isfile
        selector.op_exists = os.path.exists = _exists
        util.__import__ = _import

    def test_lint(self):
        """Test that main API functions exist
        """
        l = self.l
        l.loadTestsFromTestCase
        l.loadTestsFromModule
        l.loadTestsFromName
        l.loadTestsFromNames

    def test_load_from_name_dir_abs(self):
        print "load from name dir"
        l = self.l
        suite = l.loadTestsFromName(safepath('/a/dir/path'))
        tests = [t for t in suite]
        self.assertEqual(len(tests), 1)

    def test_load_from_name_module_filename(self):
        print "load from name module filename"
        l = self.l
        suite = l.loadTestsFromName('test_module.py')
        tests = [t for t in suite]
        assert tests

    def test_load_from_name_module(self):
        print "load from name module"
        l = self.l
        suite = l.loadTestsFromName('test_module')
        tests = [t for t in suite]
        assert tests            

    def test_load_from_name_nontest_module(self):
        print "load from name nontest module"
        l = self.l
        suite = l.loadTestsFromName('module')
        tests = [t for t in suite]
        assert tests

    def test_load_from_name_method(self):
        print "load from name method"
        res = unittest.TestResult()
        l = self.l
        suite = l.loadTestsFromName(':TC.runTest')
        tests = [t for t in suite]
        assert tests
        for test in tests:
            test(res)
        assert res.errors, \
               "Expected a ValueError for unresolvable test name, got none"

    def test_load_from_name_module_class(self):
        print "load from name module class"
        l = self.l
        suite = l.loadTestsFromName('test_module:TC')
        tests = [t for t in suite]
        print tests
        assert tests
        assert len(tests) == 1, \
               "Should have loaded 1 test, but got %s" % tests

        # the item in tests is a suite, we want to check that all of
        # the members of the suite are wrapped -- though this is really
        # a suite test and doesn't belong here..
        assert filter(lambda t: isinstance(t, nose.case.Test), tests[0])

    def test_load_from_name_module_func(self):
        print "load from name module func"
        l = self.l
        suite = l.loadTestsFromName('test_module:test_func')
        tests = [t for t in suite]
        assert tests
        assert len(tests) == 1, \
               "Should have loaded 1 test, but got %s" % tests
        assert isinstance(tests[0].test, nose.case.FunctionTestCase), \
               "Expected FunctionTestCase not %s" % tests[0].test

    def test_load_from_name_module_method(self):
        print "load from name module method"
        l = self.l
        suite = l.loadTestsFromName('test_module:TC.runTest')
        tests = [t for t in suite]
        assert tests
        assert len(tests) == 1, \
               "Should have loaded 1 test, but got %s" % tests

    def test_load_from_name_module_missing_class(self):
        print "load from name module missing class"
        res = unittest.TestResult()
        l = self.l
        suite = l.loadTestsFromName('test_module:TC2')
        tests = [t for t in suite]
        assert len(tests) == 1, \
               "Should have loaded 1 test, but got %s" % tests
        tests[0](res)
        assert res.errors, "Expected missing class test to raise exception"

    def test_load_from_name_module_missing_func(self):
        print "load from name module missing func"
        res = unittest.TestResult()
        l = self.l
        suite = l.loadTestsFromName('test_module:test_func2')
        tests = [t for t in suite]
        assert len(tests) == 1, \
               "Should have loaded 0 test, but got %s" % tests
        tests[0](res)
        assert res.errors, "Expected missing func test to raise exception"

    def test_load_from_name_module_missing_method(self):
        print "load from name module missing method"
        res = unittest.TestResult()
        l = self.l
        suite = l.loadTestsFromName('test_module:TC.testThat')
        tests = [t for t in suite]
        assert len(tests) == 1, \
               "Should have loaded 1 test, but got %s" % tests
        tests[0](res)
        assert res.errors, "Expected missing method test to raise exception"

    def test_load_from_name_missing_module(self):
        print "load from name missing module"
        res = unittest.TestResult()
        l = self.l
        suite = l.loadTestsFromName('other_test_module')
        tests = [t for t in suite]
        assert len(tests) == 1, \
               "Should have loaded 1 test, but got %s" % tests
        tests[0](res)
        assert res.errors, "Expected missing module test to raise exception"

    def test_cases_from_testcase_are_wrapped(self):
        print "cases from testcase are wrapped"
        test_module = M['test_module']
        l = self.l
        suite = l.loadTestsFromTestCase(test_module.TC)
        print suite
        tests = [t for t in suite]
        for test in tests:
            assert isinstance(test, nose.case.Test), \
                   "Test %r is not a test wrapper" % test

    def test_load_test_func(self):
        print "load test func"
        l = self.l
        suite = l.loadTestsFromName('test_module')
        tests = [t for t in suite]
        self.assertEqual(len(tests), 2, "Wanted 2 tests, got %s" % tests)
        assert filter(lambda t: isinstance(t, nose.case.Test), tests)
        print tests
        class_tests = tests[0]
        for t in class_tests:
            print "class test: ", t
        func_tests = tests[1:]
        assert class_tests, \
               "Expected class suite got %s" % class_tests
        assert len(func_tests) == 1, \
               "Expected 1 func test got %s" % func_tests
        for test in class_tests:
            assert isinstance(test.test, unittest.TestCase), \
                   "Expected TestCase npt %s" % tests[0].test
        for test in func_tests:
            assert isinstance(test.test, nose.case.FunctionTestCase), \
                   "Expected FunctionTestCase not %s" % tests[1].test

    def test_load_from_name_package_root_path(self):
        print "load from name package root path"
        l = self.l
        suite = l.loadTestsFromName(safepath('/package'))
        print suite
        tests = [t for t in suite]
        assert len(tests) == 1, "Expected one test, got %s" % tests
        tests = list(tests[0])
        assert not tests, "The full test list %s was not empty" % tests

    def test_load_from_name_subpackage_safepath(self):
        print "load from name subpackage path"
        l = self.l
        suite = l.loadTestsFromName(safepath('/package/subpackage'))
        print suite
        tests = [t for t in suite]
        assert len(tests) == 0, "Expected no tests, got %s" % tests
    
    def test_load_metaclass_customized_classes(self):
        print "load metaclass-customized classes"
        test_module_with_generators = M['test_module_with_metaclass_tests']
        l = self.l
        suite = l.loadTestsFromModule(test_module_with_generators)
        tc = [t for t in suite][0]
        tc_methods = [m for m in tc]
        self.assertEqual(len(tc_methods), 2)

    def test_load_generators(self):
        print "load generators"
        test_module_with_generators = M['test_module_with_generators']
        l = self.l
        suite = l.loadTestsFromModule(test_module_with_generators)
        tests = [t for t in suite]

        for t in tests:
            print "test", t
            assert isinstance(t, unittest.TestSuite), \
                   "Test %s is not a suite" % t

        # the first item is a class, with both normal and generator methods
        count = 0
        cl_tests = [t for t in tests[0]]
        print "class tests", cl_tests
        normal, gens = cl_tests[0], cl_tests[1:]
        assert isinstance(normal, nose.case.Test), \
               "Expected a test case but got %s" % normal
        for gen in gens:
            assert isinstance(gen, unittest.TestSuite), \
                   "Expected a generator test suite, but got %s" % gen
            count = 0
            for t in gen:
                print "generated test %s" % t
                print t.shortDescription()
                assert isinstance(t, nose.case.Test), \
                       "Test %s is not a test?" % t
                count += 1
            self.assertEqual(count, 4, "Expected to generate 4 tests, but "
                             "got %s from %s" % (count, gen))
            
        # 2nd item is generated from test_func_generator
        count = 0
        for t in tests[1]:
            print "generated test %s" % t
            print t.shortDescription()
            assert isinstance(t, nose.case.Test), \
                   "Test %s is not a Test?" % t
            assert isinstance(t.test, nose.case.FunctionTestCase), \
                   "Test %s is not a FunctionTestCase" % t.test
            assert 'test_func_generator' in str(t), \
                   "Bad str val '%s' for test" % str(t)
            assert 'docstring for test func generator' \
                   in t.shortDescription(), \
                   "Bad shortDescription '%s' for test %s" % \
                   (t.shortDescription(), t)
            count += 1
        assert count == 4, \
               "Expected to generate 4 tests, but got %s" % count

        count = 0
        for t in tests[2]:
            print "generated test %s" % t
            print t.shortDescription()
            assert isinstance(t, nose.case.Test), \
                   "Test %s is not a Test?" % t
            assert isinstance(t.test, nose.case.FunctionTestCase), \
                   "Test %s is not a FunctionTestCase" % t.test
            assert 'test_func_generator_name' in str(t), \
                   "Bad str val '%s' for test" % str(t)
            assert 'docstring for test func generator name' \
                   in t.shortDescription(), \
                   "Bad shortDescription '%s' for test %s" % \
                   (t.shortDescription(), t)
            count += 1
        assert count == 4, \
               "Expected to generate 4 tests, but got %s" % count
        
if __name__ == '__main__':
    #import logging
    #logging.basicConfig(level=logging.DEBUG)
    unittest.main()
