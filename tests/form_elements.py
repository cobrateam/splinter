# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import re
import time

import pytest

from splinter.exceptions import ElementDoesNotExist


def skip_if_zope(f):
    def wrapper(self, *args, **kwargs):
        if self.__class__.__name__ == "TestZopeTestBrowserDriver":
            return pytest.skip("skipping this test for zope testbrowser")
        else:
            f(self, *args, **kwargs)

    return wrapper


def skip_if_django(f):
    def wrapper(self, *args, **kwargs):
        if self.__class__.__name__ == "TestDjangoClientDriver":
            return pytest.skip("skipping this test for django")
        else:
            f(self, *args, **kwargs)

    return wrapper


class FormElementsTest:
    def test_fill(self):
        my_input = "LT-CS-01/2018"
        elem = self.browser.find_by_name("query")
        elem.fill(my_input)
        assert my_input == elem.value

    def test_fill_element(self):
        self.browser.find_by_name("q").fill("new query")
        time.sleep(1)
        value = self.browser.find_by_name("q").value
        assert "new query" == value

    @skip_if_zope
    def test_clicking_submit_input_doesnt_post_input_value_if_name_not_present(self):
        self.browser.find_by_css("input.submit-input-no-name").click()
        assert self.browser.find_by_xpath("/descendant-or-self::*").text.strip() == ""

    @skip_if_zope
    def test_clicking_submit_input_posts_empty_value_if_value_not_present(self):
        self.browser.find_by_css('input[name="submit-input-no-value"]').click()
        body_text = self.browser.find_by_xpath("/descendant-or-self::*").text.strip()
        assert re.match(r"^submit-input-no-value:(?:| Submit| Submit Query)$", body_text), repr(body_text)

    @skip_if_zope
    def test_clicking_submit_input_doesnt_post_input_value_if_empty(self):
        self.browser.find_by_css("input.submit-input-empty").click()
        assert self.browser.find_by_xpath("/descendant-or-self::*").text.strip() == ""

    def test_clicking_submit_input_posts_input_value_if_value_present(self):
        self.browser.find_by_css('input[name="submit-input"]').click()
        assert self.browser.find_by_xpath("/descendant-or-self::*").text == "submit-input: submit-input-value"

    @skip_if_zope
    def test_clicking_submit_button_doesnt_post_button_value_if_name_not_present(self):
        self.browser.find_by_css("button.submit-button-no-name").click()
        assert self.browser.find_by_xpath("/descendant-or-self::*").text == ""

    @skip_if_zope
    def test_clicking_submit_button_posts_empty_value_if_value_not_present(self):
        self.browser.find_by_css('button[name="submit-button-no-value"]').click()
        assert self.browser.find_by_xpath("/descendant-or-self::*").text.strip() == "submit-button-no-value:"

    @skip_if_zope
    def test_clicking_submit_button_doesnt_post_button_value_if_empty(self):
        self.browser.find_by_css("button.submit-button-empty").click()
        assert self.browser.find_by_xpath("/descendant-or-self::*").text.strip() == ""

    @skip_if_zope
    def test_clicking_submit_button_posts_button_value_if_value_present(self):
        self.browser.find_by_css('button[name="submit-button"]').click()

        assert self.browser.find_by_xpath("/descendant-or-self::*").text == "submit-button: submit-button-value"

    def test_submiting_a_form_and_verifying_page_content(self):
        self.browser.find_by_name("query").fill("my name")
        self.browser.find_by_name("send").click()
        assert "My name is: Master Splinter" in self.browser.html

    def test_can_choose_a_radio_button(self):
        "should provide a way to choose a radio button"
        assert not self.browser.find_by_id("gender-m").checked
        self.browser.choose("gender", "M")
        assert self.browser.find_by_id("gender-m").checked

    def test_can_find_textarea_by_tag(self):
        "should provide a way to find a textarea by tag_name"
        tag = self.browser.find_by_tag("textarea").first
        assert "" == tag.value

    def test_can_find_input_without_type(self):
        "should recognize an input element that doesn't have a `type` attribute"
        tag = self.browser.find_by_css('[name="typeless"]').first
        assert "default value" == tag.value

    def test_can_find_button(self):
        "should recognize a button"
        tag = self.browser.find_by_css(".just-a-button").first
        assert hasattr(tag, "click")

    def test_can_find_option_by_value(self):
        "should provide a way to find select option by value"
        assert "Rio de Janeiro" == self.browser.find_option_by_value("rj").text

    def test_can_get_value_attribute_for_a_option(self):
        "should option have a value attribute"
        assert "rj" == self.browser.find_option_by_value("rj")["value"]

    def test_can_find_option_by_text(self):
        "should provide a way to find select option by text"
        assert "rj" == self.browser.find_option_by_text("Rio de Janeiro").value

    def test_can_select_a_option(self):
        "should provide a way to select a option"
        assert not self.browser.find_option_by_value("rj").selected
        self.browser.select("uf", "rj")
        assert self.browser.find_option_by_value("rj").selected

    def test_can_select_an_option_in_an_optgroup(self):
        "should provide a way to select an option that is in an optgroup"
        assert self.browser.find_by_name("food").value == "apples"
        self.browser.select("food", "grapes")
        assert self.browser.find_by_name("food").value == "grapes"

    def test_can_select_a_option_via_element(self):
        "should provide a way to select a option via element"
        assert not self.browser.find_option_by_value("rj").selected
        self.browser.find_by_name("uf").select("rj")
        assert self.browser.find_option_by_value("rj").selected

    def test_can_check_a_checkbox(self):
        """should provide a way to check a radio checkbox"""
        elem = self.browser.find_by_name("some-check")
        assert not elem.checked
        elem.check()
        assert elem.checked

    def test_check_keeps_checked_if_called_multiple_times(self):
        """should keep a checkbox checked if check() is called multiple times"""
        elem = self.browser.find_by_name("some-check")
        assert not elem.checked
        elem.check()
        elem.check()
        assert elem.checked

    def test_can_uncheck_a_checkbox(self):
        """should provide a way to uncheck a radio checkbox"""
        elem = self.browser.find_by_name("checked-checkbox")
        assert elem.checked
        elem.uncheck()
        assert not elem.checked

    def test_uncheck_should_keep_unchecked_if_called_multiple_times(self):
        """should keep a checkbox unchecked if uncheck() is called multiple times"""
        elem = self.browser.find_by_name("checked-checkbox")
        assert elem.checked
        elem.uncheck()
        elem.uncheck()
        assert not elem.checked

    def test_can_fill_text_field_in_form(self):
        "should provide a away to change field value"
        self.browser.fill_form({"query": "new query"})
        value = self.browser.find_by_name("query").value
        assert "new query" == value

    def test_can_fill_password_field_in_form(self):
        "should provide a way to change password value"
        new_password = "new password"
        self.browser.fill_form({"password": new_password})
        value = self.browser.find_by_name("password").value
        assert new_password == value

    def test_can_fill_more_than_one_field_in_form(self):
        "should provide a away to change field value"
        self.browser.find_by_name("query").fill("my name")
        assert not self.browser.find_by_id("gender-m").checked
        assert not self.browser.find_option_by_value("rj").selected
        assert not self.browser.find_by_name("some-check").checked
        assert self.browser.find_by_name("checked-checkbox").checked
        self.browser.fill_form(
            {
                "query": "another new query",
                "description": "Just another description value in the textarea",
                "gender": "M",
                "uf": "rj",
                "some-check": True,
                "checked-checkbox": False,
            },
        )
        query_value = self.browser.find_by_name("query").value
        assert "another new query" == query_value
        desc_value = self.browser.find_by_name("description").value
        assert "Just another description value in the textarea" == desc_value
        assert self.browser.find_by_id("gender-m").checked
        assert self.browser.find_option_by_value("rj").selected
        assert self.browser.find_by_name("some-check").checked
        assert not self.browser.find_by_name("checked-checkbox").checked

    def test_can_fill_tel_text_field(self):
        "should provide a way to change a tel field value"
        new_telephone = "555-0042"
        self.browser.fill_form({"telephone": new_telephone})
        value = self.browser.find_by_name("telephone").value
        assert new_telephone == value

    def test_can_fill_unknown_text_field(self):
        "should provide a way to change a unknown text field type that isn't specifically defined"
        new_search_keyword = "foobar"
        self.browser.fill_form({"search_keyword": new_search_keyword})
        value = self.browser.find_by_name("search_keyword").value
        assert new_search_keyword == value

    def test_can_fill_form_by_id(self):
        "should be able to fill a form by its id"
        self.browser.fill_form(
            {"firstname": "John", "lastname": "Doe"},
            form_id="login",
        )
        value = self.browser.find_by_name("firstname").value
        assert "John" == value

    def test_fill_form_missing_values(self):
        """Missing values should raise an error."""
        with pytest.raises(ElementDoesNotExist) as e:
            self.browser.fill_form(
                {"query": "new query", "missing_form": "doesn't exist"},
            )

        assert "missing_form" in str(e.value)

    def test_fill_form_missing_values_ignore_missing(self):
        """Missing values are ignores when ignore_missing is True."""
        self.browser.fill_form(
            {"query": "new query", "missing_form": "doesn't exist"},
            ignore_missing=True,
        )
        value = self.browser.find_by_name("query").value
        assert "new query" == value

    def test_can_clear_text_field_content(self):
        my_input = "random query"
        elem = self.browser.find_by_name("query")
        elem.fill(my_input)
        assert my_input == elem.value

        elem.clear()
        assert not elem.value

    def test_can_clear_password_field_content(self):
        my_input = "1nF4m310"
        elem = self.browser.find_by_name("password")
        elem.fill(my_input)
        assert my_input == elem.value

        elem.clear()
        assert not elem.value

    def test_can_clear_tel_field_content(self):
        my_input = "5553743980"
        elem = self.browser.find_by_name("telephone")
        elem.fill(my_input)
        assert my_input == elem.value

        elem.clear()
        assert not elem.value

    @skip_if_django
    def test_can_clear_textarea_content(self):
        elem = self.browser.find_by_name("description")
        elem.fill("A box of widgets")
        assert "A box of widgets" == elem.value

        elem.clear()
        assert "" == elem.value

    @skip_if_django
    def test_can_clear_search_content(self):
        elem = self.browser.find_by_name("search_keyword")
        elem.fill("widgets")
        assert "widgets" == elem.value

        elem.clear()
        assert "" == elem.value

    @skip_if_django
    def test_can_clear_url_content(self):
        elem = self.browser.find_by_name("url_input")
        elem.fill("http://widgets.com")
        assert "http://widgets.com" == elem.value

        elem.clear()
        assert "" == elem.value
