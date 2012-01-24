# -*- coding: utf-8 -*-

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import ChromeCookieManager


class WebDriver(BaseWebDriver):
    def __init__(self, user_agent=None):
        self._patch_subprocess()
        options = Options()

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        self.driver = Chrome(chrome_options=options)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = ChromeCookieManager(self.driver)

        super(WebDriver, self).__init__()

    def attach_file(self, name, value):
        """
        Chrome doesn't have support for file uploading.
        """
        raise NotImplementedError
