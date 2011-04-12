print "*** test_pak imported"
state = []

def setup():
    # print "SETUP CALLED", state, id(state)
    state.append('test_pak.setup')


def teardown():
    # print "TEARDOWN CALLED", state, id(state)
    state.append('test_pak.teardown')
