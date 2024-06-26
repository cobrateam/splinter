from urllib import parse
from urllib.request import urlopen

import pytest

from tests.fake_webapp_server import start_server, stop_server

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


def pytest_configure(config):
    start_server()


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

    kwargs = {}

    if option.webdriver_remote_name:
        kwargs = {"browser": request.config.option.webdriver_remote_name}

    if option.browser_name == "flask":
        from tests.fake_webapp import app

        kwargs = {"app": app, "wait_time": 0.1}

    if option.browser_name == "django":
        components = parse.urlparse("http://127.0.0.1:5000/")
        kwargs = {
            "wait_time": 0.1,
            "client_SERVER_NAME": components.hostname,
            "client_SERVER_PORT": components.port,
        }

    wd_options = None
    if (browser_name == "chrome") or (option.webdriver_remote_name == "chrome"):
        wd_options = webdriver.chrome.options.Options()
        wd_options.add_argument("--disable-dev-shm-usage")
        kwargs["options"] = wd_options
    elif browser_name == "edge" or (option.webdriver_remote_name == "edge"):
        wd_options = webdriver.edge.options.Options()
        wd_options.add_argument("--disable-dev-shm-usage")
        kwargs["options"] = wd_options

    return kwargs


@pytest.fixture(scope="function")
def browser(browser_name, browser_config, browser_kwargs, request):
    b = Browser(browser_name, config=browser_config, **browser_kwargs)
    request.addfinalizer(b.quit)

    if not request.config.option.webdriver_fullscreen:
        if browser_name in ["chrome", "firefox", "edge"]:
            b.driver.set_window_size(1024, 768)

    return b


@pytest.fixture(scope="session")
def app_url():
    return "http://127.0.0.1:5000/"
