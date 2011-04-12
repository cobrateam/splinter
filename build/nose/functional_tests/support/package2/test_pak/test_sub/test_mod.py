from test_pak import state
import maths

def setup():
    state.append('test_pak.test_sub.test_mod.setup')

def test():
    state.append('test_pak.test_sub.test_mod.test')
    assert maths.add(1, 2) == 3

class TestMaths:

    def setup_class(cls):
        state.append('test_pak.test_sub.test_mod.TestMaths.setup_class')
    setup_class = classmethod(setup_class)

    def teardown_class(cls):
        state.append('test_pak.test_sub.test_mod.TestMaths.teardown_class')
    teardown_class = classmethod(teardown_class)
    
    def setup(self):
        state.append('test_pak.test_sub.test_mod.TestMaths.setup')

    def teardown(self):
        state.append('test_pak.test_sub.test_mod.TestMaths.teardown')
        
    def test_div(self):
        state.append('test_pak.test_sub.test_mod.TestMaths.test_div')
        assert maths.div(2, 1) == 2, "%s != %s" % (maths.div(2, 1), 2)

    def test_two_two(self):
        state.append('test_pak.test_sub.test_mod.TestMaths.test_two_two')
        assert maths.mult(2, 2) == maths.add(2, 2)
    
def teardown():
    state.append('test_pak.test_sub.test_mod.teardown')    
