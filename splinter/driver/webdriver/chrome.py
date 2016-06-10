# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from splinter.driver.webdriver import BaseWebDriver, WebDriverElement
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):

    driver_name = "Chrome"

    def __init__(self, user_agent=None, wait_time=2, fullscreen=False,
                 chrome_options=None, extensions=None, **kwargs):

        options = Options()

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if fullscreen:
            options.add_argument('--kiosk')

        if chrome_options is not None:
            for option in chrome_options:
                options.add_argument(option)

        if extensions is not None:
            for extension in extensions:
                options.add_extension(extension)

        self.driver = Chrome(chrome_options=options, **kwargs)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)
