import os
from urllib import parse

# Catch for when non-webdriver set of tests are run.
try:
    from selenium import webdriver
except ModuleNotFoundError:
    pass

from splinter import Browser

from .fake_webapp import app, EXAMPLE_APP


def get_browser(browser_name, **kwargs):
    if browser_name in ['chrome', 'chrome_fullscreen']:
        if browser_name == 'chrome_fullscreen':
            kwargs['fullscreen'] = True
        options = webdriver.chrome.options.Options()
        options.add_argument("--disable-dev-shm-usage")

        return Browser(
            "chrome",
            headless=True,
            options=options,
            **kwargs
        )

    elif browser_name in ['firefox', 'firefox_fullscreen']:
        if browser_name == 'firefox_fullscreen':
            kwargs['fullscreen'] = True

        return Browser(
            "firefox",
            headless=True,
            **kwargs
        )

    elif browser_name == 'remote':
        return Browser("remote")

    elif browser_name == 'django':
        components = parse.urlparse(EXAMPLE_APP)
        return Browser(
            "django",
            wait_time=0.1,
            client_SERVER_NAME=components.hostname,
            client_SERVER_PORT=components.port,
        )

    elif browser_name == 'flask':
        return Browser("flask", app=app, wait_time=0.1)

    elif browser_name == 'zope.testbrowser':
        return Browser("zope.testbrowser", wait_time=0.1)

    elif browser_name == 'edge':
        # Github Actions Windows EdgeDriver path
        driver_path = os.getenv('EDGEWEBDRIVER')
        if driver_path:
            kwargs['executable_path'] = driver_path + '\msedgedriver.exe'  # NOQA

        return Browser('edge', headless=True, **kwargs)

    raise ValueError('Unknown browser name')
