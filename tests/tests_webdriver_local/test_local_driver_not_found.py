import pytest

from selenium.common.exceptions import WebDriverException


def test_webdriver_local_driver_not_found(browser_name):
    """When chromedriver/geckodriver/edgedriver are not present on the system."""
    from splinter import Browser

    if browser_name == "chrome":
        from selenium.webdriver.chrome.service import Service as ChromeService

        service = ChromeService(executable_path="failpath")
    elif browser_name == "firefox":
        from selenium.webdriver.firefox.service import Service as FirefoxService

        service = FirefoxService(executable_path="failpath")
    elif browser_name == "edge":
        from selenium.webdriver.edge.service import Service as EdgeService

        service = EdgeService(executable_path="failpath")

    with pytest.raises(WebDriverException):
        Browser(browser_name, service=service)
