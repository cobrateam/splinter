import os
import unittest

class TestIssue006(unittest.TestCase):
    def test_load_nested_generator(self):
        from nose.config import Config
        from nose.loader import TestLoader

        where = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'support', 'issue006'))
        l = TestLoader()
        testmod = iter(l.loadTestsFromName(where)).next()
        print testmod
        testmod.setUp()

        testcase = iter(testmod).next()
        expect = [
            ['tests.Test1.test_nested_generator'],
            ['tests.Test1.test_nested_generator_mult(1,)',
             'tests.Test1.test_nested_generator_mult(2,)',
             'tests.Test1.test_nested_generator_mult(3,)'],
            ['tests.Test1.test_normal_generator(1,)',
             'tests.Test1.test_normal_generator(2,)']
            ]
        for test in testcase:
            tests = map(str, test)
            print tests
            self.assertEqual(tests, expect.pop(0))

if __name__ == '__main__':
    unittest.main()
