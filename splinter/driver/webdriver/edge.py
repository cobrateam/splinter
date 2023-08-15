# Copyright 2021 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import warnings
from typing import Optional

from selenium.webdriver import Edge
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service

from splinter.config import Config
from splinter.driver.webdriver import BaseWebDriver
from splinter.driver.webdriver.setup import _setup_edge


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

        options = Options() or options
        options.use_chromium = chromium

        self.config = config or Config(
            fullscreen=fullscreen,
            headless=headless,
            incognito=incognito,
            user_agent=user_agent,
        )

        driver = _setup_edge(
            Edge,
            config=self.config,
            options=options,
            service=service,
            **kwargs,
        )

        super().__init__(driver, wait_time)
