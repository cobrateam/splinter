class Test1(object):
    def test_nested_generator(self):
        def func():
            pass
        yield func,

    def test_nested_generator_mult(self):
        def f2(a):
            pass
        for b in range(1, 4):
            yield f2, b

    def try_something(self, a):
        pass

    def test_normal_generator(self):
        yield self.try_something, 1
        yield 'try_something', 2
        
