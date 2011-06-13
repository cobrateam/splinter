import os
from fake_webapp import start_server, stop_server

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))

def setup():
    start_server()

def teardown():
    stop_server()
