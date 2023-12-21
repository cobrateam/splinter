# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import unittest
from urllib.request import urlopen
from unittest.mock import patch

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
        with Browser("remote", browser="firefox"):
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
        with Browser("remote", browser="chrome"):
            pass

    def test_should_be_able_to_change_user_agent(self):
        "Remote should not support custom user agent"
        pass


@pytest.mark.macos
class RemoteBrowserSafariTest(WebDriverTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        # test with statement. It can't be used as simple test
        # because safari doesn't support multisessions
        with Browser("remote", browser="safari"):
            pass

        request.cls.browser = Browser("remote", browser="safari")
        request.addfinalizer(request.cls.browser.quit)

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_support_with_statement(self):
        """
        Remote should support with statement
        See setup browser
        """

    def test_should_be_able_to_change_user_agent(self):
        "Remote should not support custom user agent"
        pass

    # ------- BEGIN OF MULTISESSION TESTS -------
    # Safari doesn't support multisessions.
    # So next tests mock quit of browser.
    def get_new_browser(self):
        return self.browser

    def test_can_forward_on_history(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_can_forward_on_history()

    def test_create_and_access_a_cookie(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_create_and_access_a_cookie()

    def test_create_many_cookies_at_once_as_dict(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_create_many_cookies_at_once_as_dict()

    def test_create_some_cookies_and_delete_them_all(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_create_some_cookies_and_delete_them_all()

    def test_create_and_delete_a_cookie(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_create_and_delete_a_cookie()

    def test_create_and_delete_many_cookies(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_create_and_delete_many_cookies()

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_try_to_destroy_an_absent_cookie_and_nothing_happens()

    def test_create_and_get_all_cookies(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_create_and_get_all_cookies()

    def test_create_and_use_contains(self):
        with patch("splinter.driver.webdriver.remote.WebDriver.quit"):
            super().test_create_and_use_contains()

    # ------- END OF MULTISESSION TESTS -------

