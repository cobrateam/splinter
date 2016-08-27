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

    def __init__(self, options=None, user_agent=None, wait_time=2, fullscreen=False, incognito=False,
                 **kwargs):

        pass_options = Options() 

        if options is not None:
            for option in options:
                pass_options.add_argument(option)

        if user_agent is not None:
            pass_options.add_argument("--user-agent=" + user_agent)
            
        if incognito:
            pass_options.add_argument("--incognito")

        if fullscreen:
            pass_options.add_argument('--kiosk')

        self.driver = Chrome(chrome_options=pass_options, **kwargs)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)
