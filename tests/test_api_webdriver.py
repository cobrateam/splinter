from splinter.driver import WebDriver
from ludibrio import Mock, Stub


def test_visit():
    """
    WebDriver.visit should call browser.get
    """
    with Stub() as firefox:
        from selenium.firefox.webdriver import WebDriver as firefox
        with Mock() as mock:
            mock.get('http://foo.com') >> 'bar'
        firefox() >> mock
    driver = WebDriver()
    driver.visit('http://foo.com')
    mock.validate()
