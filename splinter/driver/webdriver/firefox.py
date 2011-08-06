#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):
    old_popen = subprocess.Popen

    def __init__(self, profile=None, extensions=None):
        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference('extensions.logging.enabled', 'false')

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)

        self._patch_subprocess()
        self.driver = Firefox(firefox_profile)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__()
