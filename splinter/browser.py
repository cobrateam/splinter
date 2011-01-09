from splinter.driver.webdriver.firefox import WebDriver as FirefoxWebDriver
from splinter.driver.webdriver.chrome import WebDriver as ChromeWebDriver
from splinter.driver.zopetestbrowser import ZopeTestBrowser

_DRIVERS = {'webdriver.firefox': FirefoxWebDriver,
            'zope.testbrowser': ZopeTestBrowser,
            'webdriver.chrome': ChromeWebDriver}


def Browser(driver_name='webdriver.firefox'):
    driver = _DRIVERS[driver_name]
    return driver()
