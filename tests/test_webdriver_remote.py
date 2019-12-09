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

import pytest


def selenium_server_is_running():
    try:
        from splinter.driver.webdriver.remote import WebDriver

        page_contents = urlopen(WebDriver.DEFAULT_URL).read()
    except IOError:
        return False
    return "WebDriver Hub" in page_contents


class RemoteBrowserTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = Browser("remote")
        request.addfinalizer(request.cls.browser.quit)

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_support_with_statement(self):
        "Remote should support with statement"
        with Browser("remote"):
            pass

    def test_should_be_able_to_change_user_agent(self):
        "Remote should not support custom user agent"
        pass
