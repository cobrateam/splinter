from nose import SkipTest

raise SkipTest("Don't run me")

def test():
    assert False, "Should not be run"

def test2():
    assert False, "Should not be run"
