from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
from splinter.exceptions import DriverNotFoundError

_DRIVERS = {
    'webdriver.firefox': FirefoxWebDriver,
    'webdriver.chrome': ChromeWebDriver
}

try:
    from splinter.driver.zopetestbrowser import ZopeTestBrowser
    _DRIVERS['zope.testbrowser'] = ZopeTestBrowser
except ImportError:
    pass


def Browser(driver_name='webdriver.firefox'):

    try:
        driver = _DRIVERS[driver_name]
        return driver()
    except KeyError:
        raise DriverNotFoundError
