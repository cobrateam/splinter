from test_pak import state

def setup():
    # print "SUB setup called", state, id(state)
    state.append('test_pak.test_sub.setup')

def teardown():
    # print "SUB teardown called", state, id(state)
    state.append('test_pak.test_sub.teardown')
