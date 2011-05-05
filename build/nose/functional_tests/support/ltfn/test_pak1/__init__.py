from state import called

def setup():
    called.append('test_pak1.setup')

def teardown():
    called.append('test_pak1.teardown')

def test_one_one():
    called.append('test_pak1.test_one_one')

def test_one_two():
    called.append('test_pak1.test_one_two')
