# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

from splinter import Browser
from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests
from selenium.common.exceptions import WebDriverException


def chrome_installed():
    try:
        Browser("chrome")
    except WebDriverException:
        return False
    return True


@unittest.skipIf(not chrome_installed(), 'chrome is not installed')
class ChromeBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("chrome")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'mockfile.txt'
        )
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').click()

        html = self.browser.html
        assert 'text/plain' in html
        assert open(file_path).read().encode('utf-8') in html

    def test_should_support_with_statement(self):
        with Browser('chrome') as internet:
            pass


@unittest.skipIf(not chrome_installed(), 'chrome is not installed')
class ChromeBrowserFullscreenTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("chrome", fullscreen=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_should_support_with_statement(self):
        with Browser('chrome', fullscreen=True) as internet:
            pass

    def test_with_extension(self):
        extensions = list()
        extensions.append('does_not_exist.crx')
        with self.assertRaises(OSError):
            Browser('chrome', extensions=extensions)
