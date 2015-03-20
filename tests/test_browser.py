# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

try:
    import __builtin__ as builtins
except ImportError:
    import builtins
import unittest
from imp import reload
import sys

from splinter.exceptions import DriverNotFoundError

from .fake_webapp import EXAMPLE_APP
from .test_webdriver_chrome import chrome_installed
from .test_webdriver_firefox import firefox_installed


class BrowserTest(unittest.TestCase):

    def patch_driver(self, pattern):
        self.old_import = builtins.__import__

        def custom_import(name, *args, **kwargs):
            if pattern in name:
                return None
            return self.old_import(name, *args, **kwargs)

        builtins.__import__ = custom_import

    def unpatch_driver(self, module):
        builtins.__import__ = self.old_import
        reload(module)

    def browser_can_change_user_agent(self, webdriver):
        from splinter import Browser
        browser = Browser(driver_name=webdriver, user_agent="iphone")
        browser.visit(EXAMPLE_APP + "useragent")
        result = 'iphone' in browser.html
        browser.quit()

        return result

    def test_brower_can_still_be_imported_from_splinters_browser_module(self):
        from splinter.browser import Browser

    def test_should_work_even_without_zope_testbrowser(self):
        self.patch_driver('zope')
        from splinter import browser
        reload(browser)
        self.assertNotIn('zope.testbrowser', browser._DRIVERS)
        self.unpatch_driver(browser)

    def test_should_raise_an_exception_when_browser_driver_is_not_found(self):
        with self.assertRaises(DriverNotFoundError):
            from splinter import Browser
            Browser('unknown-driver')

    @unittest.skipIf(not firefox_installed(), 'firefox is not installed')
    def test_firefox_should_be_able_to_change_user_agent(self):
        self.assertTrue(self.browser_can_change_user_agent('firefox'))

    @unittest.skipIf(not chrome_installed(), 'chrome is not installed')
    def test_chrome_should_be_able_to_change_user_agent(self):
        self.assertTrue(self.browser_can_change_user_agent('chrome'))

    @unittest.skipIf(sys.version_info[0] > 2,
                     'zope.testbrowser is not currently compatible with Python 3')
    def test_zope_testbrowser_should_be_able_to_change_user_agent(self):
        self.assertTrue(self.browser_can_change_user_agent('zope.testbrowser'))
