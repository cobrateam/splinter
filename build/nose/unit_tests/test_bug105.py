import os
import unittest

class TestBug105(unittest.TestCase):

    def test_load_in_def_order(self):
        from nose.loader import TestLoader

        where = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             'support', 'bug105'))

        l = TestLoader()
        testmod = l.loadTestsFromDir(where).next()
        print testmod
        testmod.setUp()

        def fix(t):
            s = str(t)
            if ': ' in s:
                return s[s.index(': ')+2:]
            return s
        
        tests = map(fix, testmod)
        print tests
        self.assertEqual(tests, ['tests.test_z', 'tests.test_a',
                                 'tests.test_dz', 'tests.test_mdz',
                                 'tests.test_b'])


if __name__ == '__main__':
    unittest.main()
        
