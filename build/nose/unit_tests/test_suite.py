from nose.config import Config
from nose import case
from nose.suite import LazySuite, ContextSuite, ContextSuiteFactory, \
     ContextList
import imp
import sys
import unittest
from mock import ResultProxyFactory, ResultProxy


class TestLazySuite(unittest.TestCase):

    def setUp(self):
        class TC(unittest.TestCase):
            def test_one(self):
                pass
            def test_two(self):
                pass
        self.TC = TC
        
    def test_test_generator(self):
        TC = self.TC
        tests = [TC('test_one'), TC('test_two')]
        def gen_tests():
            for test in tests:
                yield test
        suite = LazySuite(gen_tests)
        self.assertEqual(list([test for test in suite]), tests)

    def test_lazy_and_nonlazy(self):
        TC = self.TC
        tests = [TC('test_one'), TC('test_two')]
        def gen_tests():
            for test in tests:
                yield test

        nonlazy = LazySuite(tests)
        lazy = LazySuite(gen_tests)

        assert lazy
        assert nonlazy

        lazytests = []
        nonlazytests = []
        for t in lazy:
            print "lazy %s" % t
            lazytests.append(t)
        for t in nonlazy:
            print "nonlazy %s" % t
            nonlazytests.append(t)
        slazy = map(str, lazytests)
        snonlazy = map(str, nonlazytests)
        assert slazy == snonlazy, \
               "Lazy and Nonlazy produced different test lists (%s vs %s)" \
               % (slazy, snonlazy)

    def test_lazy_nonzero(self):
        """__nonzero__ works correctly for lazy suites"""
        
        TC = self.TC
        tests = [TC('test_one'), TC('test_two')]
        def gen_tests():
            for test in tests:
                yield test

        lazy = LazySuite(gen_tests)
        assert lazy
        assert lazy
        assert lazy

        count = 0
        for test in lazy:
            print test
            assert test
            count += 1
        self.assertEqual(count, 2, "Expected 2 tests, got %s" % count)
        assert lazy

        def gen_tests_empty():
            for test in []:
                yield test
            return
        empty = LazySuite(gen_tests_empty)
        assert not empty
        for test in empty:
            assert False, "Loaded a test from empty suite: %s" % test

class TestContextSuite(unittest.TestCase):

    def setUp(self):
        class TC(unittest.TestCase):
            def test_one(self):
                pass
            def test_two(self):
                pass
        self.TC = TC

    def test_tests_are_wrapped(self):
        """Tests in a context suite are wrapped"""
        suite = ContextSuite(
            [self.TC('test_one'), self.TC('test_two')])
        for test in suite:
            assert isinstance(test.test, self.TC)

    def test_nested_context_suites(self):
        """Nested suites don't re-wrap"""
        suite = ContextSuite(
            [self.TC('test_one'), self.TC('test_two')])
        suite2 = ContextSuite(suite)
        suite3 = ContextSuite([suite2])

        # suite3 is [suite2]
        tests = [t for t in suite3]
        assert isinstance(tests[0], ContextSuite)
        # suite2 is [suite]
        tests = [t for t in tests[0]]
        assert isinstance(tests[0], ContextSuite)
        # suite is full of wrapped tests
        tests = [t for t in tests[0]]
        cases = filter(lambda t: isinstance(t, case.Test), tests)
        assert cases
        assert len(cases) == len(tests)

        # sub-suites knows they have a context
        #assert suite.context is None
        #assert suite2.context is suite
        #assert suite3.context is suite2

    def test_context_fixtures_called(self):
        class P:
            was_setup = False
            was_torndown = False
            def setup(self):
                self.was_setup = True

            def teardown(self):
                self.was_torndown = True

        context = P()
        suite = ContextSuite(
            [self.TC('test_one'), self.TC('test_two')],
            context=context)
        res = unittest.TestResult()
        suite(res)

        assert not res.errors, res.errors
        assert not res.failures, res.failures
        assert context.was_setup
        assert context.was_torndown

    def test_context_fixtures_for_ancestors(self):
        top = imp.new_module('top')
        top.bot = imp.new_module('top.bot')
        top.bot.end = imp.new_module('top.bot.end')

        sys.modules['top'] = top
        sys.modules['top.bot'] = top.bot
        sys.modules['top.bot.end'] = top.bot.end

        class TC(unittest.TestCase):
            def runTest(self):
                pass
        top.bot.TC = TC
        TC.__module__ = 'top.bot'

        # suite with just TC test
        # this suite should call top and top.bot setup
        csf = ContextSuiteFactory()
        suite = csf(ContextList([TC()], context=top.bot))

        suite.setUp()
        assert top in csf.was_setup, "Ancestor not set up"
        assert top.bot in csf.was_setup, "Context not set up"
        suite.has_run = True
        suite.tearDown()
        assert top in csf.was_torndown, "Ancestor not torn down"
        assert top.bot in csf.was_torndown, "Context not torn down"

        # wrapped suites
        # the outer suite sets up its context, the inner
        # its context only, without re-setting up the outer context
        csf = ContextSuiteFactory()
        inner_suite = csf(ContextList([TC()], context=top.bot)) 
        suite = csf(ContextList(inner_suite, context=top))

        suite.setUp()
        assert top in csf.was_setup
        assert not top.bot in csf.was_setup
        inner_suite.setUp()
        assert top in csf.was_setup
        assert top.bot in csf.was_setup
        assert csf.was_setup[top] is suite
        assert csf.was_setup[top.bot] is inner_suite

    def test_context_fixtures_setup_fails(self):
        class P:
            was_setup = False
            was_torndown = False
            def setup(self):
                self.was_setup = True
                assert False, "Setup failed"

            def teardown(self):
                self.was_torndown = True

        context = P()
        suite = ContextSuite(
            [self.TC('test_one'), self.TC('test_two')],
            context=context)
        res = unittest.TestResult()
        suite(res)

        assert not res.failures, res.failures
        assert res.errors, res.errors
        assert context.was_setup
        assert not context.was_torndown
        assert res.testsRun == 0, \
               "Expected to run no tests but ran %s" % res.testsRun

    def test_context_fixtures_no_tests_no_setup(self):
        class P:
            was_setup = False
            was_torndown = False
            def setup(self):
                self.was_setup = True

            def teardown(self):
                self.was_torndown = True

        context = P()
        suite = ContextSuite([], context=context)
        res = unittest.TestResult()
        suite(res)

        assert not res.failures, res.failures
        assert not res.errors, res.errors
        assert not context.was_setup
        assert not context.was_torndown
        assert res.testsRun == 0, \
               "Expected to run no tests but ran %s" % res.testsRun

    def test_result_proxy_used(self):
        class TC(unittest.TestCase):
            def runTest(self):
                raise Exception("error")
            
        ResultProxy.called[:] = []
        res = unittest.TestResult()
        config = Config()

        suite = ContextSuite([TC()], resultProxy=ResultProxyFactory())
        suite(res)
        calls = [ c[0] for c in ResultProxy.called ]
        self.assertEqual(calls, ['beforeTest', 'startTest',
                                 'addError', 'stopTest', 'afterTest'])


class TestContextSuiteFactory(unittest.TestCase):
            
    def test_ancestry(self):
        top = imp.new_module('top')
        top.bot = imp.new_module('top.bot')
        top.bot.end = imp.new_module('top.bot.end')
        
        sys.modules['top'] = top
        sys.modules['top.bot'] = top.bot
        sys.modules['top.bot.end'] = top.bot.end
        
        class P:
            pass
        top.bot.P = P
        P.__module__ = 'top.bot'

        csf = ContextSuiteFactory()
        P_ancestors = list([a for a in csf.ancestry(P)])
        self.assertEqual(P_ancestors, [top.bot, top])

        end_ancestors = list([a for a in csf.ancestry(top.bot.end)])
        self.assertEqual(end_ancestors, [top.bot, top])

        bot_ancestors = list([a for a in csf.ancestry(top.bot)])
        self.assertEqual(bot_ancestors, [top])

        top_ancestors = list([a for a in csf.ancestry(top)])
        self.assertEqual(top_ancestors, [])


if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
        
#     class TC(unittest.TestCase):
#             def runTest(self):
#                 raise Exception("error")
            
#     ResultProxy.called[:] = []
#     res = unittest.TestResult()
#     config = Config()

    
