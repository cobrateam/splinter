from selenium.chrome.webdriver import WebDriver as chrome_driver
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement as BaseWebDriverElement


class WebDriver(BaseWebDriver):

    def __init__(self):
        self.driver = chrome_driver()
        self.element_class = WebDriverElement

    def attach_file(self, name, value):
        raise NotImplementedError

class WebDriverElement(BaseWebDriverElement):

    def _get_value(self):
        if self._element.get_value():
            return self._element.get_value()
        else:
            return self._element.get_text()

    def _set_value(self, value):
        self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)
