from splinter.driver import WebDriver
from ludibrio import Mock, Stub


def test_visit():
    """
    WebDriver.visit should call browser.get
    """
    with Mock() as mock:
        mock.get('http://foo.com')
    with Stub() as browser:
        from selenium.firefox.webdriver import WebDriver as browser
        browser() >> mock
    driver = WebDriver()
    driver.visit('http://foo.com')
    browser.restore_import()
    mock.validate()


def test_title():
    """
    WebDriver.title should call browser.get_title
    """
    with Mock() as mock:
        mock.get_title()
    with Stub() as browser:
        from selenium.firefox.webdriver import WebDriver as browser
        browser() >> mock
    driver = WebDriver()
    driver.title
    browser.restore_import()
    mock.validate()


def test_quit():
    """
    WebDriver.quit should call browser.quit
    """
    with Mock() as mock:
        mock.quit()
    with Stub() as browser:
        from selenium.firefox.webdriver import WebDriver as browser
        browser() >> mock
    driver = WebDriver()
    driver.quit()
    browser.restore_import()
    mock.validate()