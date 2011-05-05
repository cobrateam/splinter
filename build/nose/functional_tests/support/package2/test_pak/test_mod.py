print "test_mod imported!"

import maths
from test_pak import state

def setup():
    print "MOD setup called", state, id(state)
    state.append('test_pak.test_mod.setup')

def test_add():
    print "MOD.test_add called", state, id(state)
    state.append('test_pak.test_mod.test_add')
    assert maths.add(1, 2) == 3

def test_minus():
    state.append('test_pak.test_mod.test_minus')
    
def teardown():
    print "MOD teardown called", state, id(state)
    state.append('test_pak.test_mod.teardown')
