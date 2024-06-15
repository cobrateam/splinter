import pytest

from selenium.common.exceptions import WebDriverException


def test_webdriver_local_driver_not_found(browser_name):
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
