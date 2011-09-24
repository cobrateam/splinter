# -*- coding: utf-8 -*-

from __future__ import with_statement

import __builtin__

try:
    import unittest2 as unittest
except ImportError:
    import unittest

import warnings

from splinter.exceptions import DriverNotFoundError
from splinter.utils import deprecate_driver_class


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

    def test_should_work_even_without_zope_testbrowser(self):
        self.patch_driver('zope')
        from splinter import browser
        reload(browser)
        assert 'zope.testbrowser' not in browser._DRIVERS, 'zope.testbrowser driver should not be registered when zope.testbrowser is not installed'
        self.unpatch_driver(browser)

    def test_should_raise_an_exception_when_browser_driver_is_not_found(self):
        with self.assertRaises(DriverNotFoundError):
            from splinter.browser import Browser
            Browser('unknown-driver')


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
            self.assertEquals("Foo was deprecated", warning.message.args[0])

    def test_should_prepend_a_Deprecated_to_class(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('default')
            cls = deprecate_driver_class(self.Foo, message="Foo was deprecated")
            self.assertEquals("DeprecatedFoo", cls.__name__)

    def test_webdriverfirefox_should_be_deprecated(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('default')
            from splinter.browser import Browser
            browser = Browser('webdriver.firefox')
            browser.quit()
            warning_message = warnings_list[0].message.args[0]
            self.assertEquals("'webdriver.firefox' is deprecated, use just 'firefox'", warning_message)

    def test_webdriverchrome_should_be_deprecated(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('default')
            from splinter.browser import Browser
            browser = Browser('webdriver.chrome')
            browser.quit()
            warning_message = warnings_list[0].message.args[0]
            self.assertEquals("'webdriver.chrome' is deprecated, use just 'chrome'", warning_message)
