from fake_webapp import start_server, stop_server

def setup():
    start_server()

def teardown():
    stop_server()
