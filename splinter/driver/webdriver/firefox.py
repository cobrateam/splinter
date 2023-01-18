# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import warnings
from typing import Optional

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from splinter.driver.webdriver import BaseWebDriver


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
        service: Optional[Service] = None,
        **kwargs
    ):

        if 'executable_path' in kwargs:
            warnings.warn(
                (
                    "Webdriver's executable_path argument has been deprecated."
                    "Please pass in a selenium Service object instead."
                ),
                DeprecationWarning,
                stacklevel=2,
            )
            if service is None:
                service = Service(executable_path=kwargs['executable_path'])
            else:
                service.executable_path = kwargs['executable_path']

        options = options or Options()
        if profile:
            options.set_preference("profile", profile)
        options.set_preference("extensions.logging.enabled", False)
        options.set_preference("network.dns.disableIPv6", False)

        if capabilities:
            for key, value in capabilities.items():
                options.set_capability(key, value)

        if user_agent is not None:
            options.set_preference("general.useragent.override", user_agent)

        if profile_preferences:
            for key, value in profile_preferences.items():
                options.set_preference(key, value)

        if headless:
            options.add_argument("--headless")

        if incognito:
            options.add_argument("-private")

        driver = Firefox(
            options=options,
            service=service,
            **kwargs,
        )

        if extensions:
            for extension in extensions:
                driver.install_addon(extension)

        if fullscreen:
            driver.fullscreen_window()

        super(WebDriver, self).__init__(driver, wait_time)
