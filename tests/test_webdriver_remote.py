# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from unittest.mock import patch
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


class TestRemoteBrowserFirefox(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = Browser("remote", browser="firefox")
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)

    def test_support_with_statement(self):
        "Remote should support with statement"
        with Browser("remote", browser="firefox"):
            pass

    @pytest.mark.skip(reason="Remote should not support custom user agent")
    def test_should_be_able_to_change_user_agent(self):
        pass


class TestRemoteBrowserChrome(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = Browser("remote", browser="chrome")
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)

    def test_support_with_statement(self):
        "Remote should support with statement"
        with Browser("remote", browser="chrome"):
            pass

    @pytest.mark.skip(reason="Remote should not support custom user agent")
    def test_should_be_able_to_change_user_agent(self):
        pass


@pytest.mark.macos
class TestRemoteBrowserSafari(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        # test with statement. It can't be used as simple test
        # because safari doesn't support multisessions
        with Browser("remote", browser="safari"):
            pass

        request.cls.browser = Browser("remote", browser="safari")
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)

    def test_support_with_statement(self):
        """
        Remote should support with statement
        See setup browser
        """

    @pytest.mark.skip(reason="Remote should not support custom user agent")
    def test_should_be_able_to_change_user_agent(self):
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

    def test_can_fill_more_than_one_field_in_form(self):
        "should provide a away to change field value"
        self.browser.find_by_name("query").fill("my name")
        assert not self.browser.find_by_id("gender-m").checked
        assert not self.browser.find_option_by_value("rj").selected
        assert not self.browser.find_by_name("some-check").checked
        assert self.browser.find_by_name("checked-checkbox").checked
        # Select of dropdown doesn't work for Safari 17 (remote). Safari as OS user works well
        # for some reason select doesn't work for Safari
        self.browser.fill_form(
            {
                "query": "another new query",
                "description": "Just another description value in the textarea",
                "gender": "M",
                # "uf": "rj",
                "some-check": True,
                "checked-checkbox": False,
            },
        )
        query_value = self.browser.find_by_name("query").value
        assert "another new query" == query_value
        desc_value = self.browser.find_by_name("description").value
        assert "Just another description value in the textarea" == desc_value
        assert self.browser.find_by_id("gender-m").checked
        # assert self.browser.find_option_by_value("rj").selected
        assert self.browser.find_by_name("some-check").checked
        assert not self.browser.find_by_name("checked-checkbox").checked

    # ------- BEGIN OF CLICK PROBLEM TESTS -------
    # https://stackoverflow.com/questions/77388720/automation-testing-with-selenium-click-doesnt-works-on-new-safari-17-ios-sonoma
    @pytest.mark.xfail
    def test_click_element_by_css_selector(self):
        super().test_click_element_by_css_selector()

    @pytest.mark.xfail
    def test_click_input_by_css_selector(self):
        super().test_click_input_by_css_selector()

    @pytest.mark.xfail
    def test_clicking_submit_button_doesnt_post_button_value_if_empty(self):
        super().test_clicking_submit_button_doesnt_post_button_value_if_empty()

    @pytest.mark.xfail
    def test_clicking_submit_button_doesnt_post_button_value_if_name_not_present(self):
        super().test_clicking_submit_button_doesnt_post_button_value_if_name_not_present()

    @pytest.mark.xfail
    def test_clicking_submit_button_posts_button_value_if_value_present(self):
        super().test_clicking_submit_button_posts_button_value_if_value_present()

    @pytest.mark.xfail
    def test_clicking_submit_button_posts_empty_value_if_value_not_present(self):
        super().test_clicking_submit_button_posts_empty_value_if_value_not_present()

    @pytest.mark.xfail
    def test_clicking_submit_input_doesnt_post_input_value_if_empty(self):
        super().test_clicking_submit_input_doesnt_post_input_value_if_empty()

    @pytest.mark.xfail
    def test_clicking_submit_input_doesnt_post_input_value_if_name_not_present(self):
        super().test_clicking_submit_input_doesnt_post_input_value_if_name_not_present()

    @pytest.mark.xfail
    def test_clicking_submit_input_posts_empty_value_if_value_not_present(self):
        super().test_clicking_submit_input_posts_empty_value_if_value_not_present()

    @pytest.mark.xfail
    def test_clicking_submit_input_posts_input_value_if_value_present(self):
        super().test_clicking_submit_input_posts_input_value_if_value_present()

    @pytest.mark.xfail
    def test_submiting_a_form_and_verifying_page_content(self):
        super().test_submiting_a_form_and_verifying_page_content()

    @pytest.mark.xfail
    def test_click_links(self):
        super().test_click_links()

    # ------- END OF CLICK PROBLEM TESTS -------
    # ------- START OF TYPE PROBLEM TESTS -------
    @pytest.mark.xfail
    def test_simple_type(self):
        super().test_simple_type()

    @pytest.mark.xfail
    def test_simple_type_on_element(self):
        super().test_simple_type_on_element()

    # ------- END OF TYPE PROBLEM TESTS -------
