# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import unittest
from urllib.request import urlopen

import pytest

from .base import WebDriverTests
from .fake_webapp import EXAMPLE_APP
from splinter import Browser


def selenium_server_is_running():
    try:
        from splinter.driver.webdriver.remote import WebDriver

        page_contents = urlopen(WebDriver.DEFAULT_URL).read()
    except OSError:
        return False
    return "WebDriver Hub" in page_contents


class RemoteBrowserFirefoxTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = Browser("remote", browser="firefox")
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


class RemoteBrowserChromeTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = Browser("remote", browser="chrome")
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


@pytest.mark.macos
class RemoteBrowserSafariTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = Browser("remote", browser="safari")
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
