import os
import unittest

class TestIssue230(unittest.TestCase):

    def test_generator_yield_value(self):
        from nose.loader import TestLoader

        def test():
            pass
        def gen():
            yield test

        loader = TestLoader()
        suite = loader.loadTestsFromGenerator(gen, module=None)
        testcase = iter(suite).next()
        self.assertEqual(testcase.test.test, test)


if __name__ == '__main__':
    unittest.main()
