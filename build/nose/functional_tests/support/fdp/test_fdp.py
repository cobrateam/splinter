def test_err():
    raise TypeError("I can't type")

def test_fail():
    print "Hello"
    a = 2
    assert a == 4, "a is not 4"

def test_ok():
    pass
