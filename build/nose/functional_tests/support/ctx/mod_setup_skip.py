from nose import SkipTest

def setup():
    raise SkipTest("no thanks")


def test_a():
    raise AssertionError("test_a should not run")


def test_b():
    raise AssertionError("test_b should not run")


