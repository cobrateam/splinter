# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from selenium.webdriver import Remote
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from splinter.driver.webdriver import BaseWebDriver
from splinter.cookie_manager import CookieManagerAPI
from splinter.driver.webdriver.remote import WebDriverElement

def config_browserstack(os, os_version, browser, browser_version, debug=False, local=False, **ability_args):
    # fill capabilities config
    ability = {
        'os': os,
        'os_version': os_version,
        'browser': browser,
        'browser_version': browser_version
    }

    if debug:
        ability['browserstack.debug'] = True

    if local:
        ability['browserstack.local'] = True

    ability.update(ability_args)

    return ability

class WebDriver(BaseWebDriver):

    driver_name = "Browserstack webdriver"
    URL_PATTERN = 'http://%(username)s:%(password)s@hub.browserstack.com:80/wd/hub'
    _browserstack = None

    def _setup_browserstack(self, username, password, url_pattern=URL_PATTERN):
        self._browserstack = {
            'username': username,
            'password': password
        }
        url = url_pattern % self._browserstack
        self._browserstack['remote_url'] = url
        return url

    def __init__(self, username, password, wait_time=2, **ability_args):
        if 'browser' not in ability_args:
            raise ValueError('browser argument is not present.')

        url = self._setup_browserstack(username, password)
        browser_name = ability_args['browser'].upper()
        if browser_name == 'IE':
            browser_name = 'INTERNETEXPLORER'
        abilities = getattr(DesiredCapabilities, browser_name, {})
        abilities.update(ability_args)
        self.driver = Remote(url, abilities)

        self.element_class = WebDriverElement

        self._cookie_manager = CookieManagerAPI()

        super(WebDriver, self).__init__(wait_time)