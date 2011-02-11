from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver

try:
    from splinter.driver.zopetestbrowser import ZopeTestBrowser
    has_zope_browser = True
except ImportError:
    has_zope_browser = False

_DRIVERS = {
    'webdriver.firefox': FirefoxWebDriver,
    'webdriver.chrome': ChromeWebDriver
}

if has_zope_browser:
    _DRIVERS['zope.testbrowser'] = ZopeTestBrowser

def Browser(driver_name='webdriver.firefox'):
    driver = _DRIVERS[driver_name]
    return driver()
