import os
import sys
from multiprocessing import Process
from urllib.request import urlopen

import pytest

from tests.fake_webapp import EXAMPLE_APP
from tests.fake_webapp import start_flask_app
from tests.get_browser import get_browser

import splinter
from splinter import Browser
from splinter.config import Config


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


@pytest.fixture
def get_new_browser(request):
    def new_browser(browser_name):
        browser = get_browser(browser_name)
        request.addfinalizer(browser.quit)
        return browser

    return new_browser


def pytest_addoption(parser):
    group = parser.getgroup(
        "splinter",
        "splinter integration",
    )
    group.addoption(
        "--browser",
        help="Name of the browser to use.",
        type=str,
        choices=list(splinter.browser._DRIVERS.keys()),
        dest="browser_name",
    )


@pytest.fixture(scope="session")
def browser_name(request) -> str:
    return request.config.option.browser_name


@pytest.fixture(scope="session")
def browser_config():
    return Config(headless=True)


@pytest.fixture(scope="session")
def browser_kwargs():
    return {}


@pytest.fixture(scope="function")
def browser(browser_name, browser_config, browser_kwargs):
    return Browser(browser_name, config=browser_config, **browser_kwargs)
