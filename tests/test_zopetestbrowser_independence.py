# -*- coding: utf-8 -*-

import unittest
from nose.tools import assert_false, raises
from splinter.exceptions import DriverNotFoundError


class TestZopeTestBrowserIndependence(unittest.TestCase):

    @raises(DriverNotFoundError)
    def test_should_work_even_without_zope_testbrowser(self):
        import __builtin__
        self.savimport = __builtin__.__import__
        def myimport(name, *a, **kw):
          if 'zope' in name: return
          return self.savimport(name, *a, **kw)
        __builtin__.__import__ = myimport

        from splinter import browser
        reload(browser)
        assert_false('zope.testbrowser' in browser._DRIVERS.keys())
        browser.Browser('zope.testbrowser')
