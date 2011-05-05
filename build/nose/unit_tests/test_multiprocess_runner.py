import unittest
import imp
import sys
from nose.loader import TestLoader
from nose.plugins import multiprocess
from nose.suite import ContextSuite

class T_fixt:
    def setupClass(cls):
        pass
    setupClass = classmethod(setupClass)

    def test_a(self):
        pass
    def test_b(self):
        pass
    
class T:
    def test_a(self):
        pass
    def test_b(self):
        pass



class TestMultiProcessTestRunner(unittest.TestCase):

    def test_next_batch_with_classes(self):
        r = multiprocess.MultiProcessTestRunner()
        l = TestLoader()
        tests = list(r.nextBatch(ContextSuite(
                    tests=[l.makeTest(T_fixt), l.makeTest(T)])))
        print tests
        self.assertEqual(len(tests), 3)

    def test_next_batch_with_module_fixt(self):
        mod_with_fixt = imp.new_module('mod_with_fixt')
        sys.modules['mod_with_fixt'] = mod_with_fixt

        def teardown():
            pass

        class Test(T):
            pass

        mod_with_fixt.Test = Test
        mod_with_fixt.teardown = teardown
        Test.__module__ = 'mod_with_fixt'

        r = multiprocess.MultiProcessTestRunner()
        l = TestLoader()
        tests = list(r.nextBatch(l.loadTestsFromModule(mod_with_fixt)))
        print tests
        self.assertEqual(len(tests), 1)

    def test_next_batch_with_module(self):
        mod_no_fixt = imp.new_module('mod_no_fixt')
        sys.modules['mod_no_fixt'] = mod_no_fixt

        class Test2(T):
            pass

        class Test_fixt(T_fixt):
            pass

        mod_no_fixt.Test = Test2
        Test2.__module__ = 'mod_no_fixt'
        mod_no_fixt.Test_fixt = Test_fixt
        Test_fixt.__module__ = 'mod_no_fixt'

        r = multiprocess.MultiProcessTestRunner()
        l = TestLoader()
        tests = list(r.nextBatch(l.loadTestsFromModule(mod_no_fixt)))
        print tests
        self.assertEqual(len(tests), 3)

    def test_next_batch_with_generator_method(self):
        class Tg:
            def test_gen(self):
                for i in range(0, 3):
                    yield self.check, i
            def check(self, val):
                pass
        r = multiprocess.MultiProcessTestRunner()
        l = TestLoader()
        tests = list(r.nextBatch(l.makeTest(Tg)))
        print tests
        print [r.address(t) for t in tests]
        self.assertEqual(len(tests), 1)

    def test_next_batch_can_split_set(self):

        mod_with_fixt2 = imp.new_module('mod_with_fixt2')
        sys.modules['mod_with_fixt2'] = mod_with_fixt2

        def setup():
            pass

        class Test(T):
            pass

        class Test_fixt(T_fixt):
            pass

        mod_with_fixt2.Test = Test
        mod_with_fixt2.Test_fixt = Test_fixt
        mod_with_fixt2.setup = setup
        mod_with_fixt2._multiprocess_can_split_ = True
        Test.__module__ = 'mod_with_fixt2'
        Test_fixt.__module__ = 'mod_with_fixt2'

        r = multiprocess.MultiProcessTestRunner()
        l = TestLoader()
        tests = list(r.nextBatch(l.loadTestsFromModule(mod_with_fixt2)))
        print tests
        self.assertEqual(len(tests), 3)
        
            
if __name__ == '__main__':
    unittest.main()
