from state import called

def setup():
    called.append('test_pak1.test_mod.setup')

def teardown():
    called.append('test_pak1.test_mod.teardown')

def test_one_mod_one():
    called.append('test_pak1.test_mod.test_one_mod_one')
    pass

