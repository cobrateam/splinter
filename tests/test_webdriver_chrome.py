# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests


class ChromeBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("chrome")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_attach_file_is_not_implemented(self):
        "attach file is not implemented for chrome driver"
        with self.assertRaises(NotImplementedError):
            self.browser.attach_file('file', 'file_path')
