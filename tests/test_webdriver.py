import os

import pytest
from selenium.common.exceptions import WebDriverException

from .base import supported_browsers
from .fake_webapp import EXAMPLE_APP
from .get_browser import get_browser


@pytest.mark.parametrize("browser_name", ["chrome", "firefox"])
def test_webdriver_local_driver_not_present(browser_name):
    """When chromedriver/geckodriver are not present on the system."""
    from splinter import Browser

    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.firefox.service import Service as FirefoxService

    if browser_name == "chrome":
        service = ChromeService(executable_path="failpath")
    else:
        service = FirefoxService(executable_path="failpath")

    with pytest.raises(WebDriverException):
        Browser(browser_name, service=service)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_attach_file(request, browser_name):
    """Should provide a way to change file field value"""
    browser = get_browser(browser_name)
    request.addfinalizer(browser.quit)

    file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "mockfile.txt")

    browser.visit(EXAMPLE_APP)
    browser.attach_file("file", file_path)
    browser.find_by_name("upload").click()

    html = browser.html
    assert "text/plain" in html

    with open(file_path) as f:
        assert str(f.read()) in html


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_browser_config(request, browser_name):
    """Splinter's drivers get the Config object when it's passed through the Browser function."""
    from splinter import Config

    config = Config(user_agent="agent_smith")
    browser = get_browser(browser_name, config=config)
    request.addfinalizer(browser.quit)

    assert browser.config.user_agent == "agent_smith"
