def my_decor(func):
    return lambda: func()

def test_decor():
    pass

def test_decor1():
    pass
test_decor1 = my_decor(test_decor1)
