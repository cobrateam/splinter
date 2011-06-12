# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement


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
