# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome, DesiredCapabilities
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import ChromeCookieManager

class WebDriver(BaseWebDriver):
    def __init__(self, user_agent=None):
        self._patch_subprocess()
        capabilities = DesiredCapabilities.CHROME

        if user_agent is not None:
            capabilities["chrome.switches"] = ["--user-agent=" + user_agent]

        self.driver = Chrome(desired_capabilities=capabilities)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = ChromeCookieManager(self.driver)

        super(WebDriver, self).__init__()

    def attach_file(self, name, value):
        """
        Chrome doesn't have support for file uploading.
        """
        raise NotImplementedError
