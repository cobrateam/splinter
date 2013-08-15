# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement as BaseWebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):

    driver_name = "Firefox"

    def __init__(self, profile=None, extensions=None, user_agent=None, profile_preferences=None, wait_time=2):
        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference('extensions.logging.enabled', False)
        firefox_profile.set_preference('network.dns.disableIPv6', False)

        if user_agent is not None:
            firefox_profile.set_preference('general.useragent.override', user_agent)

        if profile_preferences:
            for key, value in profile_preferences.items():
                firefox_profile.set_preference(key, value)

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)

        self.driver = Firefox(firefox_profile)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)


class WebDriverElement(BaseWebDriverElement):

    def mouse_over(self):
        """
        Firefox doesn't support mouseover.
        """
        raise NotImplementedError("Firefox doesn't support mouse over")

    def mouse_out(self):
        """
        Firefox doesn't support mouseout.
        """
        raise NotImplementedError("Firefox doesn't support mouseout")

    mouseover = mouse_over
    mouseout = mouse_out
