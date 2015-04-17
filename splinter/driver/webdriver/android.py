# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Android
from splinter.driver.webdriver import (
    BaseWebDriver, WebDriverElement as WebDriverElement)
from splinter.driver.webdriver.cookie_manager import CookieManager


class WebDriver(BaseWebDriver):

    driver_name = "Android"

    def __init__(self, wait_time=2):

        self.driver = Android()

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManager(self.driver)

        super(WebDriver, self).__init__(wait_time)
