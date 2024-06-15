import os
import sys
from multiprocessing import Process
from urllib import parse
from urllib.request import urlopen

import pytest

from tests.fake_webapp import EXAMPLE_APP
from tests.fake_webapp import start_flask_app

import splinter
from splinter import Browser
from splinter.config import Config

# Catch for when non-webdriver set of tests are run.
try:
    from selenium import webdriver
except ModuleNotFoundError:
    pass


def selenium_server_is_running():
    try:
        from splinter.driver.webdriver.remote import WebDriver

        page_contents = urlopen(WebDriver.DEFAULT_URL).read()
    except OSError:
        return False
    return "WebDriver Hub" in page_contents


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
    group.addoption(
        "--webdriver-remote-name",
        help="Name of the driver to use when running Remote Webdriver.",
        type=str,
        dest="webdriver_remote_name",
    )
    group.addoption(
        "--webdriver-fullscreen",
        help="Run webdriver tests in fullscreen mode.",
        type=bool,
        dest="webdriver_fullscreen",
    )


@pytest.fixture(scope="session")
def browser_name(request) -> str:
    return request.config.option.browser_name


@pytest.fixture(scope="session")
def browser_config(request):
    c = Config(headless=True)
    if request.config.option.webdriver_fullscreen:
        c.fullscreen = True
    return c


@pytest.fixture(scope="session")
def browser_kwargs(request):
    option = request.config.option

    if option.webdriver_remote_name:
        return {"browser": request.config.option.webdriver_remote_name}

    if option.browser_name == "flask":
        from tests.fake_webapp import app

        return {"app": app, "wait_time": 0.1}

    if option.browser_name == "django":
        components = parse.urlparse("http://127.0.0.1:5000/")
        return {
            "wait_time": 0.1,
            "client_SERVER_NAME": components.hostname,
            "client_SERVER_PORT": components.port,
        }

    return {}


@pytest.fixture(scope="function")
def browser(browser_name, browser_config, browser_kwargs, request):
    b = Browser(browser_name, config=browser_config, **browser_kwargs)
    request.addfinalizer(b.quit)

    if not request.config.option.webdriver_fullscreen:
        if browser_name in ["chrome", "firefox", "edge"]:
            b.driver.set_window_size(1024, 768)

    if browser_name == "chrome":
        options = webdriver.chrome.options.Options()
        options.add_argument("--disable-dev-shm-usage")

    return b


@pytest.fixture(scope="session")
def app_url():
    return "http://127.0.0.1:5000/"
