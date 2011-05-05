from nose import tools

def test_z():
    """(1) test z"""
    pass

def test_a():
    """(2) test a"""
    pass

def test_rz():
    """(3) Test with raises decorator"""
    raise TypeError("err")
test_rz = tools.raises(TypeError)(test_rz)

def decorate(func):
    func.attr = 1
    return func

def dec_replace(func):
    def newfunc():
        func()
        pass
    return newfunc

def dec_makedecorator(func):
    def newfunc():
        pass
    newfunc = tools.make_decorator(func)(newfunc)
    return newfunc

def test_dz():
    """(4) Test with non-replacing decorator"""
    pass
test_dz = decorate(test_dz)

def test_rz():
    """(5) Test with replacing decorator"""
    pass
test_rz = dec_replace(test_rz)

def test_mdz():
    """(6) Test with make_decorator decorator"""
    pass
test_mdz = dec_makedecorator(test_mdz)

def test_b():
    """(7) test b"""
    pass
