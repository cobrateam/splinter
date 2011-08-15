# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import ChromeCookieManager


class WebDriver(BaseWebDriver):
    def __init__(self):
        self._patch_subprocess()
        self.driver = Chrome()
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = ChromeCookieManager(self.driver)

        super(WebDriver, self).__init__()

    def attach_file(self, name, value):
        """
        Chrome doesn't have support for file uploading.
        """
        raise NotImplementedError
