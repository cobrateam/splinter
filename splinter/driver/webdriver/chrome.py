# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from splinter.driver.webdriver import BaseWebDriver
from splinter.driver.webdriver import WebDriverElement as BaseWebDriverElement


class WebDriver(BaseWebDriver):
    def __init__(self):
        self._patch_subprocess()
        self.driver = Chrome()
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        super(WebDriver, self).__init__()

    def attach_file(self, name, value):
        raise NotImplementedError
        
    def get_alert(self):
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
