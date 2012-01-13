#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement as BaseWebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):

    def __init__(self, profile=None, extensions=None, user_agent=None):
        self.old_popen = subprocess.Popen
        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference('extensions.logging.enabled', False)
        firefox_profile.set_preference('network.dns.disableIPv6', False)

        if user_agent is not None:
            firefox_profile.set_preference('general.useragent.override', user_agent)

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)

        self._patch_subprocess()
        self.driver = Firefox(firefox_profile)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__()


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

    def double_click(self):
        """
        Firefox doesn't support doubleclick.
        """
        raise NotImplementedError("Firefox doesn't support doubleclick")

    def right_click(self):
        """
        Firefox doesn't support right click'
        """
        raise NotImplementedError("Firefox doesn't support right click")

    def drag_and_drop(self, droppable):
        """
        Firefox doesn't support drag and drop
        """
        raise NotImplementedError("Firefox doesn't support drag an drop")

    mouseover = mouse_over
    mouseout = mouse_out
