# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from splinter import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests

import subprocess


def selenium_server_is_running():
    ps = subprocess.Popen(['ps', '-o', 'command'], stdout=subprocess.PIPE).communicate()[0]
    return 'selenium-server' in ps


@unittest.skipIf(not selenium_server_is_running(), 'Skipping the remote webdriver tests')
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
            self.browser.find_by_id('visible').first.mouse_over()

    def test_mouse_out(self):
        "Remote should not support mouseout"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').first.mouse_out()

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

    def test_mouseover_should_be_an_alias_to_mouse_over_and_be_deprecated(self):
        "Remote should not support mouseover"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').mouseover()

    def test_mouseout_should_be_an_alias_to_mouse_out_and_be_deprecated(self):
        "Remote should not support mouseout"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').mouseout()

    def test_create_and_access_a_cookie(self):
        "Remote should not support cookies"
        with self.assertRaises(NotImplementedError):
            self.browser.cookies.add({'sha': 'zam'})

    def test_create_some_cookies_and_delete_them_all(self):
        "Remote should not support cookies"
        with self.assertRaises(NotImplementedError):
            self.browser.cookies.delete()

    def test_create_and_delete_a_cookie(self):
        "Remote should not support cookies"
        with self.assertRaises(NotImplementedError):
            self.browser.cookies.delete('cookie')

    def test_create_and_delete_many_cookies(self):
        "Remote should not support cookies"
        with self.assertRaises(NotImplementedError):
            self.browser.cookies.delete('cookie', 'notacookie')

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        "Remote should not support cookies"
        with self.assertRaises(NotImplementedError):
            self.browser.cookies.delete('mwahahahaha')
