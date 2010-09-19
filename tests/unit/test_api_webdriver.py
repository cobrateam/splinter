from splinter.driver import WebDriver
from ludibrio import Mock, Stub


class replace_browser:

    def __init__(self, driver_mock):
        with Stub() as browser:
            from selenium.firefox.webdriver import WebDriver as browser
            browser() >> driver_mock
        self.browser = browser

    def __enter__(self):pass

    def __exit__(self, type, value, traceback):
        self.browser.restore_import()


def test_visit():
    """
    WebDriver.visit should call browser.get
    """
    with Mock() as firefox_mock:
        firefox_mock.get('http://foo.com')

    with replace_browser(firefox_mock):
        driver = WebDriver()
        driver.visit('http://foo.com')

    firefox_mock.validate()


def test_title():
    """
    WebDriver.title should call browser.title
    """
    with Mock() as firefox_mock:
        firefox_mock.get_title() >> None

    with replace_browser(firefox_mock):
        driver = WebDriver()
        driver.title

    firefox_mock.validate()


def test_quit():
    """
    WebDriver.quit should call browser.quit
    """
    with Mock() as firefox_mock:
        firefox_mock.quit()

    with replace_browser(firefox_mock):
        driver = WebDriver()
        driver.quit()

    firefox_mock.validate()


