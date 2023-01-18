# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import warnings
from typing import Optional

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from splinter.driver.webdriver import BaseWebDriver


class WebDriver(BaseWebDriver):

    driver_name = "Chrome"

    def __init__(
        self,
        options=None,
        user_agent=None,
        wait_time=2,
        fullscreen=False,
        incognito=False,
        headless=False,
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

        if user_agent is not None:
            options.add_argument("--user-agent=" + user_agent)

        if incognito:
            options.add_argument("--incognito")

        if fullscreen:
            options.add_argument("--kiosk")

        if headless:
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")

        driver = Chrome(options=options, service=service, **kwargs)

        super(WebDriver, self).__init__(driver, wait_time)
