#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from selenium.webdriver import Remote
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement as BaseWebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):

    def __init__(self, server, port=4443, profile=None, extensions=None):
        self.old_popen = subprocess.Popen
        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference('extensions.logging.enabled', False)
        firefox_profile.set_preference('network.dns.disableIPv6', False)

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)

        self._patch_subprocess()
        dest = 'http://%s:%s/wd/hub'%(server,port)
        self.driver = Remote(dest, {}, firefox_profile)
        self._unpatch_subprocess()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__()


class WebDriverElement(BaseWebDriverElement):

    def mouse_over(self):
        """
        Remote Firefox doesn't support mouseover.
        """
        raise NotImplementedError("Remote Firefox doesn't support mouse over")

    def mouse_out(self):
        """
        Remote Firefox doesn't support mouseout.
        """
        raise NotImplementedError("Remote Firefox doesn't support mouseout")

    def double_click(self):
        """
        Remote Firefox doesn't support doubleclick.
        """
        raise NotImplementedError("Remote Firefox doesn't support doubleclick")

    def right_click(self):
        """
        Remote Firefox doesn't support right click'
        """
        raise NotImplementedError("Remote Firefox doesn't support right click")

    def drag_and_drop(self, droppable):
        """
        Remote Firefox doesn't support drag and drop
        """
        raise NotImplementedError("Remote Firefox doesn't support drag an drop")

    mouseover = mouse_over
    mouseout = mouse_out
