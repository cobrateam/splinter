import os
import pathlib

import pytest
from selenium.common.exceptions import WebDriverException

from tests.fake_webapp import EXAMPLE_APP


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


def test_attach_file(request, browser):
    """Should provide a way to change file field value"""
    request.addfinalizer(browser.quit)

    file_path = pathlib.Path(
        os.getcwd(),  # NOQA PTH109
        "tests",
        "mockfile.txt",
    )

    browser.visit(EXAMPLE_APP)
    browser.attach_file("file", str(file_path))
    browser.find_by_name("upload").click()

    html = browser.html
    assert "text/plain" in html

    with open(file_path) as f:
        assert str(f.read()) in html


def test_browser_config(request, browser_name):
    """Splinter's drivers get the Config object when it's passed through the Browser function."""
    from splinter import Config
    from splinter import Browser

    config = Config(user_agent="agent_smith", headless=True)
    browser = Browser(browser_name, config=config)
    request.addfinalizer(browser.quit)

    assert browser.config.user_agent == "agent_smith"
