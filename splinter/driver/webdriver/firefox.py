# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os, sys
from subprocess import check_output

from selenium.webdriver import DesiredCapabilities, Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from splinter.driver.webdriver import (
    BaseWebDriver, WebDriverElement as WebDriverElement)
from splinter.driver.webdriver.cookie_manager import CookieManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class WebDriver(BaseWebDriver):

    driver_name = "Firefox"

    def __init__(self, profile=None, extensions=None, user_agent=None,
                 profile_preferences=None, fullscreen=False, wait_time=2,
                 capabilities=None, firefox_binary_path=None):

        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference('extensions.logging.enabled', False)
        firefox_profile.set_preference('network.dns.disableIPv6', False)

        firefox_capabilities = DesiredCapabilities().FIREFOX

        if capabilities:
            for key, value in capabilities.items():
                firefox_capabilities[key] = value

        if user_agent is not None:
            firefox_profile.set_preference(
                'general.useragent.override', user_agent)

        if profile_preferences:
            for key, value in profile_preferences.items():
                firefox_profile.set_preference(key, value)

        if extensions:
            for extension in extensions:
                firefox_profile.add_extension(extension)
        
        firefox_binary = None
        if firefox_binary_path is not None:
            firefox_binary = FirefoxBinary(firefox_path=firefox_binary_path)
        else:
            firefox_binary = self._guess_firefox_path_if_sensible()
        
        self.driver = Firefox(firefox_profile,
                              capabilities=firefox_capabilities,
                              firefox_binary=firefox_binary)

        if fullscreen:
            ActionChains(self.driver).send_keys(Keys.F11).perform()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)

    def _guess_firefox_path_if_sensible(self):
        # Selenium guesses really badly (i.e. not at all) where Firefox on os x is installed.
        # So let's ask the system instead
        standard_firefox_path = "/Applications/Firefox.app/Contents/MacOS/firefox-bin"
        if not sys.platform.startswith('darwin') \
            or os.path.isfile(standard_firefox_path):
            return None
        
        path = check_output(["mdfind", "kMDItemFSName = Firefox.app"]).decode('utf-8').strip()
        if path == '': return None
        
        if len(path.split()) > 1: # found multiple foxes, just take the first one
            # if you need more control, specify manually
            # TODO consider some logging?
            path = path.split()[0]
        
        firefox_binary_path = os.path.join(path, "Contents/MacOS/firefox-bin")
        return FirefoxBinary(firefox_path=firefox_binary_path)
    