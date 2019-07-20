# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

import pytest

from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests, get_browser
from selenium.common.exceptions import WebDriverException


def chrome_installed():
    try:
        Browser("chrome")
    except WebDriverException:
        return False
    return True


class ChromeBase(object):
    @pytest.fixture(autouse=True, scope='class')
    def teardown(self, request):
        request.addfinalizer(self.browser.quit)


class ChromeBrowserTest(WebDriverTests, ChromeBase, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('chrome', fullscreen=False)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.driver.set_window_size(1024, 768)
        self.browser.visit(EXAMPLE_APP)

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "mockfile.txt"
        )
        self.browser.attach_file("file", file_path)
        self.browser.find_by_name("upload").click()

        html = self.browser.html
        self.assertIn("text/plain", html)

        with open(file_path) as f:
            expected = str(f.read().encode("utf-8"))

        self.assertIn(expected, html)

    def test_should_support_with_statement(self):
        with get_browser('chrome'):
            pass


class ChromeBrowserFullscreenTest(WebDriverTests, ChromeBase, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('chrome', fullscreen=True)

    @pytest.fixture(autouse=True)
    def visit_example_app(self):
        self.browser.visit(EXAMPLE_APP)

    def test_should_support_with_statement(self):
        with get_browser('chrome', fullscreen=True):
            pass
