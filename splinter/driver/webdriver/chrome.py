# -*- coding: utf-8 -*-
from selenium.webdriver.chrome.webdriver import WebDriver as chrome_driver

from splinter.driver.webdriver import BaseWebDriver
from splinter.driver.webdriver import WebDriverElement as BaseWebDriverElement


class WebDriver(BaseWebDriver):
    def __init__(self):
        self._patch_subprocess()
        self.driver = chrome_driver()
        self._unpatch_subprocess()

        self.element_class = WebDriverElement
        
        super(WebDriver, self).__init__()

    def attach_file(self, name, value):
        raise NotImplementedError

class WebDriverElement(BaseWebDriverElement):

    def _get_value(self):
        if self._element.value:
            return self._element.value
        else:
            return self._element.text

    def _set_value(self, value):
        self._element.clear()
        self._element.send_keys(value)

    value = property(_get_value, _set_value)
