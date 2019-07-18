import sys

import os

from multiprocessing import Process

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen

from tests.fake_webapp import start_flask_app, EXAMPLE_APP


class Env(object):
    def __init__(self):
        self.process = None
        self.host = 'localhost'
        self.port = 5000


env = Env()


def wait_until_start():
    while True:
        try:
            results = urlopen(EXAMPLE_APP)
            if results.code == 404:
                raise Exception("%s returned unexpected 404" % EXAMPLE_APP)
            break
        except IOError:
            pass


def wait_until_stop():
    while True:
        try:
            results = urlopen(EXAMPLE_APP)
            if results.code == 404:
                break
        except IOError:
            break


def start_server():
    sys.stderr = open(os.devnull, "w")
    env.process = Process(target=start_flask_app, args=(env.host, env.port))
    env.process.daemon = True
    env.process.start()
    wait_until_start()


def stop_server():
    env.process.terminate()
    env.process.join()
    wait_until_stop()


def pytest_configure(config):
    try:
        start_server()
    except Exception as e:
        sys.stdout.write("Failed to start test server: %s\n\n" % e)
        sys.exit(1)


def pytest_unconfigure(config):
    stop_server()
