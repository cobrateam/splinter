# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from splinter.driver.webdriver import BaseWebDriver
from selenium.webdriver.firefox.options import Options


class WebDriver(BaseWebDriver):

    driver_name = "Firefox"

    def __init__(
        self,
        options=None,
        profile=None,
        extensions=None,
        user_agent=None,
        profile_preferences=None,
        fullscreen=False,
        wait_time=2,
        capabilities=None,
        headless=False,
        incognito=False,
        **kwargs
    ):

        firefox_profile = FirefoxProfile(profile)
        firefox_profile.set_preference("extensions.logging.enabled", False)
        firefox_profile.set_preference("network.dns.disableIPv6", False)

        options = options or Options()

        if capabilities:
            for key, value in capabilities.items():
                options.set_capability(key, value)

        if user_agent is not None:
            options.set_preference("general.useragent.override", user_agent)

        if profile_preferences:
            for key, value in profile_preferences.items():
                firefox_profile.set_preference(key, value)

        if headless:
            options.add_argument("--headless")

        if incognito:
            options.add_argument("-private")

        driver = Firefox(
            firefox_profile,
            options=options,
            **kwargs,
        )

        if extensions:
            for extension in extensions:
                driver.install_addon(extension)

        if fullscreen:
            driver.fullscreen_window()

        super(WebDriver, self).__init__(driver, wait_time)
