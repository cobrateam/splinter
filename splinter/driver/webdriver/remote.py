# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from typing import Optional

from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote import remote_connection

from splinter.config import Config
from splinter.driver.webdriver import BaseWebDriver
from splinter.driver.webdriver.remote_connection import patch_request
from splinter.driver.webdriver.setup import _setup_chrome
from splinter.driver.webdriver.setup import _setup_edge
from splinter.driver.webdriver.setup import _setup_firefox
from splinter.driver.webdriver.setup import _setup_safari

# MonkeyPatch RemoteConnection
remote_connection.RemoteConnection._request = patch_request  # type: ignore


class WebDriver(BaseWebDriver):
    driver_name = "remote"
    # TODO: This constant belongs in selenium.webdriver.Remote
    DEFAULT_URL = "http://127.0.0.1:4444/wd/hub"

    def __init__(
        self,
        browser="firefox",
        wait_time=2,
        command_executor=DEFAULT_URL,
        options=None,
        config: Optional[Config] = None,
        **kwargs,
    ):
        browser_name = browser.upper()
        # Handle case where user specifies IE with a space in it
        if browser_name == "INTERNET EXPLORER":
            browser_name = "INTERNETEXPLORER"

        # If no desired capabilities specified, add default ones
        caps = getattr(DesiredCapabilities, browser_name, {})
        if kwargs.get("desired_capabilities"):
            # Combine user's desired capabilities with default
            caps.update(kwargs["desired_capabilities"])

            kwargs["desired_capabilities"] = caps

        kwargs["command_executor"] = command_executor

        self.config = config or Config()

        if browser_name == "CHROME":
            from selenium.webdriver.chrome.options import Options

            options = options or Options()
            driver = _setup_chrome(Remote, self.config, options, **kwargs)
        elif browser_name == "EDGE":
            from selenium.webdriver.edge.options import Options

            options = options or Options()
            driver = _setup_edge(Remote, self.config, options, **kwargs)
        elif browser_name == "FIREFOX":
            from selenium.webdriver.firefox.options import Options

            options = options or Options()
            driver = _setup_firefox(Remote, self.config, options, **kwargs)
        elif browser_name == "SAFARI":
            from selenium.webdriver.safari.options import Options

            options = options or Options()
            driver = _setup_safari(Remote, self.config, options, **kwargs)
        else:
            raise ValueError(f"Unsupporeted browser {browser_name}")

        super().__init__(driver, wait_time)
