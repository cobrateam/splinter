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
    mock.validate()
