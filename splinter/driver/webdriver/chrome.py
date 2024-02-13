# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import warnings
from typing import Optional

from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from splinter.config import Config
from splinter.driver.webdriver import BaseWebDriver
from splinter.driver.webdriver.setup import _setup_chrome


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
        config: Optional[Config] = None,
        **kwargs,
    ):
        if True in [fullscreen, incognito, headless] or user_agent:
            warnings.warn(
                (
                    "Sending fullscreen, incognito, headless, user_agent to the browser object has been deprecated."
                    "Please pass in a Splinter Config object instead."
                    "See: https://splinter.readthedocs.io/en/latest/config.html for more details"
                ),
                DeprecationWarning,
                stacklevel=2,
            )

        options = options or Options()

        self.config = config or Config(
            fullscreen=fullscreen,
            headless=headless,
            incognito=incognito,
            user_agent=user_agent,
        )

        driver = _setup_chrome(
            Chrome,
            config=self.config,
            options=options,
            service=service,
            **kwargs,
        )

        super().__init__(driver, wait_time)
