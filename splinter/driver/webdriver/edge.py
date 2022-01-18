# -*- coding: utf-8 -*-

# Copyright 2021 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

# Selenium 3 compatibility
try:
    from msedge.selenium_tools import Edge
    from msedge.selenium_tools import EdgeOptions as Options
except ImportError:
    from selenium.webdriver import Edge
    from selenium.webdriver.edge.options import Options

from splinter.driver.webdriver import BaseWebDriver


class WebDriver(BaseWebDriver):

    driver_name = "Edge"

    def __init__(
        self,
        options=None,
        user_agent=None,
        wait_time=2,
        fullscreen=False,
        incognito=False,
        headless=False,
        chromium=True,
        **kwargs
    ):

        options = Options() or options

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if incognito:
            options.add_argument("--incognito")

        if fullscreen:
            options.add_argument("--kiosk")

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        options.use_chromium = chromium

        driver = Edge(options=options, **kwargs)

        super(WebDriver, self).__init__(driver, wait_time)
