from state import called

def setup():
    called.append('test_mod.setup')

def test_mod():
    called.append('test_mod.test_mod')

def teardown():
    called.append('test_mod.teardown')
