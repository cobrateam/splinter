import multiprocessing
import os
import sys
from urllib.request import urlopen

from tests.fake_webapp import EXAMPLE_APP
from tests.fake_webapp import start_flask_app


class Env:
    def __init__(self):
        self.process = None
        self.host = "localhost"
        self.port = 5000


env = Env()


def wait_until_start():
    while True:
        try:
            results = urlopen(EXAMPLE_APP)
            if results.code == 404:
                raise Exception("%s returned unexpected 404" % EXAMPLE_APP)
            break
        except OSError:
            pass


def wait_until_stop():
    while True:
        try:
            results = urlopen(EXAMPLE_APP)
            if results.code == 404:
                break
        except OSError:
            break


def start_server():
    """Start the Flask app used for integration testing."""
    try:
        sys.stderr = open(os.devnull, "w")
        env.process = multiprocessing.Process(target=start_flask_app, args=(env.host, env.port))
        env.process.daemon = True
        env.process.start()
        wait_until_start()
    except Exception as e:
        sys.stdout.write("Failed to start test server: %s\n\n" % e)
        sys.exit(1)


def stop_server():
    """Stop the Flask app used for integration testing."""
    env.process.terminate()
    env.process.join()
    wait_until_stop()
