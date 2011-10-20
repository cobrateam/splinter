# -*- coding: utf-8 -*-

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests
from tests import Namespace

ns = Namespace()


def setUpModule():
    ns.browser = Browser('chrome')


def tearDownModule():
    ns.browser.quit()


class ChromeBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = ns.browser

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_attach_file_is_not_implemented(self):
        "attach file is not implemented for chrome driver"
        with self.assertRaises(NotImplementedError):
            self.browser.attach_file('file', 'file_path')
