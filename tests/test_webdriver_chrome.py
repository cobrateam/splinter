# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest

import pytest

from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests, get_browser


class ChromeBrowserTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('chrome', fullscreen=False)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.driver.set_window_size(1024, 768)
        self.browser.visit(EXAMPLE_APP)


class ChromeBrowserFullscreenTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('chrome', fullscreen=True)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self):
        self.browser.visit(EXAMPLE_APP)


def test_should_support_with_statement_fullscreen():
    with get_browser('chrome', fullscreen=True):
        pass
