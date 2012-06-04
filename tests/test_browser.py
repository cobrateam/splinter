# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from __future__ import with_statement

import __builtin__

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import warnings

from splinter.exceptions import DriverNotFoundError
from splinter.utils import deprecate_driver_class

from fake_webapp import EXAMPLE_APP

class BrowserTest(unittest.TestCase):

    def patch_driver(self, pattern):
        self.old_import = __builtin__.__import__

        def custom_import(name, *args, **kwargs):
              if pattern in name:
                  return None
              return self.old_import(name, *args, **kwargs)

        __builtin__.__import__ = custom_import

    def unpatch_driver(self, module):
        __builtin__.__import__ = self.old_import
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
        assert 'zope.testbrowser' not in browser._DRIVERS, 'zope.testbrowser driver should not be registered when zope.testbrowser is not installed'
        self.unpatch_driver(browser)

    def test_should_raise_an_exception_when_browser_driver_is_not_found(self):
        with self.assertRaises(DriverNotFoundError):
            from splinter import Browser
            Browser('unknown-driver')

    def test_firefox_should_be_able_to_change_user_agent(self):
        self.assertTrue(self.browser_can_change_user_agent('firefox'))

    def test_chrome_should_be_able_to_change_user_agent(self):
        self.assertTrue(self.browser_can_change_user_agent('chrome'))

    def test_zope_testbrowser_should_be_able_to_change_user_agent(self):
        self.assertTrue(self.browser_can_change_user_agent('zope.testbrowser'))

    def test_firefox_chrome_and_zope_testbrowser_should_support_with_statement(self):
        for browser in ('firefox', 'chrome', 'zope.testbrowser'):
            from splinter import Browser
            with Browser(browser) as internet:
                pass

class BrowserDeprecationTest(unittest.TestCase):

    class Foo(object):
        pass

    def test_should_deprecate_with_the_given_message(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('default')
            cls = deprecate_driver_class(self.Foo, message="Foo was deprecated")
            cls()
            warning = warnings_list[0]
            assert type(warning.message) is DeprecationWarning
            self.assertEqual("Foo was deprecated", warning.message.args[0])

    def test_should_prepend_a_Deprecated_to_class(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('default')
            cls = deprecate_driver_class(self.Foo, message="Foo was deprecated")
            self.assertEqual("DeprecatedFoo", cls.__name__)

    def test_webdriverfirefox_should_be_deprecated(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('default')
            from splinter import Browser
            browser = Browser('webdriver.firefox')
            browser.quit()
            warning_message = warnings_list[0].message.args[0]
            self.assertEqual("'webdriver.firefox' is deprecated, use just 'firefox'", warning_message)

    def test_webdriverchrome_should_be_deprecated(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('default')
            from splinter import Browser
            browser = Browser('webdriver.chrome')
            browser.quit()
            warning_message = warnings_list[0].message.args[0]
            self.assertEqual("'webdriver.chrome' is deprecated, use just 'chrome'", warning_message)

