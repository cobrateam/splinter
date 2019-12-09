# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Remote
from selenium.webdriver.remote import remote_connection
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from splinter.driver.webdriver import (
    BaseWebDriver,
    WebDriverElement,
)
from splinter.driver.webdriver.cookie_manager import CookieManager
from splinter.driver.webdriver.remote_connection import patch_request

# MonkeyPatch RemoteConnection
remote_connection.RemoteConnection._request = patch_request


class WebDriver(BaseWebDriver):

    driver_name = "remote"
    # TODO: This constant belongs in selenium.webdriver.Remote
    DEFAULT_URL = "http://127.0.0.1:4444/wd/hub"

    def __init__(
        self,
        browser="firefox",
        wait_time=2,
        command_executor=DEFAULT_URL,
        **kwargs
    ):
        browser_name = browser.upper()
        # Handle case where user specifies IE with a space in it
        if browser_name == "INTERNET EXPLORER":
            browser_name = "INTERNETEXPLORER"

        # If no desired capabilities specified, add default ones
        caps = getattr(DesiredCapabilities, browser_name, {})
        if kwargs.get('desired_capabilities'):
            # Combine user's desired capabilities with default
            caps.update(kwargs['desired_capabilities'])

        kwargs['desired_capabilities'] = caps

        self.driver = Remote(command_executor, **kwargs)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)
