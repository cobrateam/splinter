# -*- coding: utf-8 -*-

from __future__ import with_statement

import unittest
import warnings

from nose.tools import assert_equals, raises
from splinter.exceptions import DriverNotFoundError
from splinter.utils import deprecate_driver_class


class BrowserTest(unittest.TestCase):

    def test_should_work_even_without_zope_testbrowser(self):
        import __builtin__
        old_import = __builtin__.__import__

        def custom_import(name, *args, **kwargs):
              if 'zope' in name:
                  return None
              return old_import(name, *args, **kwargs)

        __builtin__.__import__ = custom_import

        from splinter import browser
        reload(browser)
        assert 'zope.testbrowser' not in browser._DRIVERS, 'zope.testbrowser driver should not be registered when zope.testbrowser is not installed'
        __builtin__.__import__ = old_import
        reload(browser)

    @raises(DriverNotFoundError)
    def test_should_raise_an_exception_when_browser_driver_is_not_found(self):
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
            assert_equals("Foo was deprecated", warning.message.args[0])

    def test_should_prepend_a_Deprecated_to_class(self):
        with warnings.catch_warnings(record=True):
            warnings.simplefilter('default')
            cls = deprecate_driver_class(self.Foo, message="Foo was deprecated")
            assert_equals("DeprecatedFoo", cls.__name__)

    def test_webdriverfirefox_should_be_deprecated(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('default')
            from splinter.browser import Browser
            browser = Browser('webdriver.firefox')
            browser.quit()
            warning_message = warnings_list[0].message.args[0]
            assert_equals("'webdriver.firefox' is deprecated, use just 'firefox'", warning_message)

    def test_webdriverchrome_should_be_deprecated(self):
        with warnings.catch_warnings(record=True) as warnings_list:
            warnings.simplefilter('default')
            from splinter.browser import Browser
            browser = Browser('webdriver.chrome')
            browser.quit()
            warning_message = warnings_list[0].message.args[0]
            assert_equals("'webdriver.chrome' is deprecated, use just 'chrome'", warning_message)
