from nose.exc import SkipTest


def test_a():
    pass


def test_b():
    raise SkipTest("I'm not ready for test b")
