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

    # Safari doesn't support multisessions.
    # So next test must be rewrited without getting new browser
    def test_can_forward_on_history(self):
        next_url = f"{EXAMPLE_APP}iframe"

        self.browser.visit(EXAMPLE_APP)
        self.browser.visit(next_url)
        self.browser.back()

        self.browser.forward()
        assert next_url == self.browser.url

    def test_create_and_access_a_cookie(self):
        """Should be able to create and access a cookie"""
        self.browser.visit(self.EXAMPLE_APP)

        self.browser.cookies.add({"sha": "zam"})

        assert "zam" == self.browser.cookies["sha"]

    def test_create_many_cookies_at_once_as_dict(self):
        """Should be able to create many cookies at once as dict"""
        self.browser.visit(self.EXAMPLE_APP)

        cookies = {"sha": "zam", "foo": "bar"}
        self.browser.cookies.add(cookies)

        assert "zam" == self.browser.cookies["sha"]
        assert "bar" == self.browser.cookies["foo"]

    def test_create_some_cookies_and_delete_them_all(self):
        """Should be able to delete all cookies"""
        self.browser.visit(self.EXAMPLE_APP)

        self.browser.cookies.add({"whatever": "and ever"})
        self.browser.cookies.add({"anothercookie": "im bored"})
        self.browser.cookies.delete_all()

        assert {} == self.browser.cookies

    def test_create_and_delete_a_cookie(self):
        """Should be able to create and destroy a cookie"""
        self.browser.visit(self.EXAMPLE_APP)

        self.browser.cookies.delete_all()
        self.browser.cookies.add({"cookie": "with milk"})
        self.browser.cookies.delete("cookie")

        assert {} == self.browser.cookies

    def test_create_and_delete_many_cookies(self):
        """Should be able to create and destroy many cookies"""
        self.browser.visit(self.EXAMPLE_APP)

        self.browser.cookies.delete_all()
        self.browser.cookies.add({"acookie": "cooked"})
        self.browser.cookies.add({"anothercookie": "uncooked"})
        self.browser.cookies.add({"notacookie": "halfcooked"})
        self.browser.cookies.delete("acookie", "notacookie")

        assert "uncooked" == self.browser.cookies["anothercookie"]

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        self.browser.visit(self.EXAMPLE_APP)

        self.browser.cookies.delete_all()
        self.browser.cookies.add({"foo": "bar"})
        self.browser.cookies.delete("mwahahahaha")

        {"foo": "bar"} == self.browser.cookies

    def test_create_and_get_all_cookies(self):
        """Should be able to create some cookies and retrieve them all"""

        self.browser.visit(self.EXAMPLE_APP)

        self.browser.cookies.delete_all()
        self.browser.cookies.add({"taco": "shrimp"})
        self.browser.cookies.add({"lavar": "burton"})

        assert 2 == len(self.browser.cookies.all())

        self.browser.cookies.delete_all()

        assert {} == self.browser.cookies.all()

    def test_create_and_use_contains(self):
        """Should be able to create many cookies at once as dict"""

        self.browser.visit(self.EXAMPLE_APP)

        cookies = {"sha": "zam"}
        self.browser.cookies.add(cookies)

        assert "sha" in self.browser.cookies
        assert "foo" not in self.browser.cookies
