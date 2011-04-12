from state import called

def setup():
    called.append('test_pak2.setup')

def teardown():
    called.append('test_pak2.teardown')
    
def test_two_one():
    called.append('test_pak2.test_two_one')

def test_two_two():
    called.append('test_pak2.test_two_two')
