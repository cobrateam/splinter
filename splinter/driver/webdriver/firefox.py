# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import warnings
from typing import Optional

from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

from splinter.config import Config
from splinter.driver.webdriver import BaseWebDriver
from splinter.driver.webdriver.setup import _setup_firefox


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
        config: Optional[Config] = None,
        **kwargs,
    ):
        if "executable_path" in kwargs:
            warnings.warn(
                (
                    "Webdriver's executable_path argument has been deprecated."
                    "Please pass in a selenium Service object instead."
                ),
                DeprecationWarning,
                stacklevel=2,
            )
            if service is None:
                service = Service(executable_path=kwargs["executable_path"])
            else:
                service.executable_path = kwargs["executable_path"]

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

        if profile:
            options.set_preference("profile", profile)
        options.set_preference("extensions.logging.enabled", False)
        options.set_preference("network.dns.disableIPv6", False)

        self.config = config or Config(
            extensions=extensions,
            fullscreen=fullscreen,
            headless=headless,
            incognito=incognito,
            user_agent=user_agent,
        )

        if capabilities:
            for key, value in capabilities.items():
                options.set_capability(key, value)

        if profile_preferences:
            for key, value in profile_preferences.items():
                options.set_preference(key, value)

        driver = _setup_firefox(
            Firefox,
            config=self.config,
            options=options,
            service=service,
            **kwargs,
        )

        super().__init__(driver, wait_time)
