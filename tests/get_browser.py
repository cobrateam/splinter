import os
from urllib import parse

# Catch for when non-webdriver set of tests are run.
try:
    from selenium import webdriver
except ModuleNotFoundError:
    pass

from splinter import Browser
from splinter.config import Config

from .fake_webapp import app, EXAMPLE_APP


def get_browser(browser_name, config=None, **kwargs):
    config = config or Config()
    config.headless = True

    if browser_name in ["chrome", "chrome_fullscreen"]:
        if browser_name == "chrome_fullscreen":
            config.fullscreen = True
        options = webdriver.chrome.options.Options()
        options.add_argument("--disable-dev-shm-usage")

        return Browser("chrome", options=options, config=config, **kwargs)

    elif browser_name in ["firefox", "firefox_fullscreen"]:
        if browser_name == "firefox_fullscreen":
            config.fullscreen = True

        return Browser("firefox", config=config, **kwargs)

    elif browser_name == "remote":
        return Browser("remote")

    elif browser_name == "django":
        components = parse.urlparse(EXAMPLE_APP)
        return Browser(
            "django",
            wait_time=0.1,
            client_SERVER_NAME=components.hostname,
            client_SERVER_PORT=components.port,
            **kwargs,
        )

    elif browser_name == "flask":
        app = kwargs.pop("app", app)
        return Browser("flask", app=app, **kwargs)

    elif browser_name == "zope.testbrowser":
        return Browser("zope.testbrowser", **kwargs)

    elif browser_name == "edge":
        # Github Actions Windows EdgeDriver path
        service = None
        driver_path = os.getenv("EDGEWEBDRIVER")
        if driver_path:
            from selenium.webdriver.edge.service import Service as EdgeService

            edgedriver_path = os.path.join(driver_path, "msedgedriver.exe")
            service = EdgeService(executable_path=edgedriver_path)

        return Browser("edge", service=service, config=config, **kwargs)

    raise ValueError("Unknown browser name")
