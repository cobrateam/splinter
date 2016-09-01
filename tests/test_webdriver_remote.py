# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen
import unittest

from splinter import Browser
from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests


def selenium_server_is_running():
    try:
        from splinter.driver.webdriver.remote import WebDriver
        page_contents = urlopen(WebDriver.DEFAULT_URL).read()
    except IOError:
        return False
    return 'WebDriver Hub' in page_contents


class RemoteBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("remote")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_support_with_statement(self):
        "Remote should support with statement"
        with Browser('remote') as remote:
            pass

    def test_mouse_over(self):
        "Remote should not support mouseover"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').mouse_over()

    def test_mouse_out(self):
        "Remote should not support mouseout"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').mouse_out()

    def test_double_click(self):
        "Remote should not support double_click"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').double_click()

    def test_right_click(self):
        "Remote should not support right_click"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').right_click()

    def test_drag_and_drop(self):
        "Remote should not support drag_and_drop"
        with self.assertRaises(NotImplementedError):
            droppable = self.browser.find_by_css('.droppable')
            self.browser.find_by_css('.draggable').drag_and_drop(droppable)

    def test_mouseover_should_be_an_alias_to_mouse_over(self):
        "Remote should not support mouseover"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').mouseover()

    def test_should_be_able_to_change_user_agent(self):
        "Remote should not support custom user agent"
        pass
