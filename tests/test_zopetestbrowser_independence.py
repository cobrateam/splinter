# -*- coding: utf-8 -*-

import unittest
from nose.tools import raises
from splinter.exceptions import DriverNotFoundError


class TestZopeTestBrowserIndependence(unittest.TestCase):

    @raises(DriverNotFoundError)
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
        browser.Browser('zope.testbrowser')
        __builtin__.__import__ = old_import
