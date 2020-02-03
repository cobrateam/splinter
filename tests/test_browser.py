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

from splinter.exceptions import DriverNotFoundError

from selenium.common.exceptions import WebDriverException

import pytest

from .fake_webapp import EXAMPLE_APP


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
        result = "iphone" in browser.html
        browser.quit()

        return result

    def test_brower_can_still_be_imported_from_splinters_browser_module(self):
        from splinter.browser import Browser  # NOQA

    def test_should_work_even_without_zope_testbrowser(self):
        self.patch_driver("zope")
        from splinter import browser

        reload(browser)
        self.assertNotIn("zope.testbrowser", browser._DRIVERS)
        self.unpatch_driver(browser)

    def test_should_raise_an_exception_when_browser_driver_is_not_found(self):
        with self.assertRaises(DriverNotFoundError):
            from splinter import Browser

            Browser("unknown-driver")


@pytest.mark.parametrize('browser_name', ['chrome', 'firefox'])
def test_local_driver_not_present(browser_name):
    """When chromedriver/geckodriver are not present on the system."""
    from splinter import Browser

    with pytest.raises(WebDriverException) as e:
        Browser(browser_name, executable_path='failpath')

    assert "Message: 'failpath' executable needs to be in PATH." in str(e.value)


def test_driver_retry_count():
    """Checks that the retry count is being used"""
    from splinter.browser import _DRIVERS
    from splinter import Browser
    global test_retry_count

    def test_driver(*args, **kwargs):
        global test_retry_count
        test_retry_count += 1
        raise IOError("test_retry_count: " + str(test_retry_count))
    _DRIVERS["test_driver"] = test_driver

    test_retry_count = 0
    with pytest.raises(IOError) as e:
        Browser("test_driver")
    assert "test_retry_count: 3" == str(e.value)

    test_retry_count = 0
    with pytest.raises(IOError) as e:
        Browser("test_driver", retry_count=10)
    assert "test_retry_count: 10" == str(e.value)

    del test_retry_count
    del _DRIVERS["test_driver"]
