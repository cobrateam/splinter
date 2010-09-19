from splinter.browser import Browser
from ludibrio import Mock, Stub

def test_visit():
    """
    Browser.visit should call driver.visit
    """
    with Mock() as mock:
        mock.visit('http://foo.com')
    with Stub() as browser:
        from splinter.driver import WebDriver
        WebDriver() >> mock
    browser = Browser()
    browser.visit('http://foo.com')

    WebDriver.restore_import()
    mock.validate()

def test_quit():
    """
    Browser.quit should call driver.quit
    """
    with Mock() as mock:
        mock.quit()
    with Stub() as browser:
        from splinter.driver import WebDriver
        WebDriver() >> mock
    browser = Browser()
    browser.quit()

    WebDriver.restore_import()
    mock.validate()