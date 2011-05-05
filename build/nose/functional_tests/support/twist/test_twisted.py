from twisted.trial import unittest

class TestTwisted(unittest.TestCase):

    def test(self):
        pass

    def test_fail(self):
        self.fail("I failed")

    def test_error(self):
        raise TypeError("oops, wrong type")

    def test_skip(self):
        raise unittest.SkipTest('skip me')
