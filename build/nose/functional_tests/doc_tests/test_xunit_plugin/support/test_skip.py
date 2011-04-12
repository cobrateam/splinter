from nose.exc import SkipTest

def test_ok():
    pass

def test_err():
    raise Exception("oh no")

def test_fail():
    assert False, "bye"

def test_skip():
    raise SkipTest("not me")
