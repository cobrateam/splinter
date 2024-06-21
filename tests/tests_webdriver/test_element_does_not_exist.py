# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from splinter.exceptions import ElementDoesNotExist


def test_element_query_should_raises_when_element_first_doest_exists(browser, app_url):
    browser.visit(app_url)
    with pytest.raises(ElementDoesNotExist):
        browser.find_by_css(".element-that-dont-exists").first


def test_element_list_raises_when_element_last_does_not_exists(browser, app_url):
    browser.visit(app_url)
    with pytest.raises(ElementDoesNotExist):
        browser.find_by_css(".element-that-dont-exists").last


def test_element_list_raises_when_element_does_not_exists(browser, app_url):
    browser.visit(app_url)
    with pytest.raises(ElementDoesNotExist):
        browser.find_by_css(".element-that-dont-exists")[2]


def test_element_list_raises_with_unicode_query(browser, app_url):
    browser.visit(app_url)
    with pytest.raises(ElementDoesNotExist):
        browser.find_by_css(".element[title=título]").last


def test_element_list_contains_right_information_and_raises_right_exception(browser, app_url):
    "element list contains right information about query and raises nice exception message"
    browser.visit(app_url)
    with pytest.raises(ElementDoesNotExist) as err:
        element_list = browser.find_by_css(".element-that-dont-exists")
        assert "css" == element_list.find_by
        assert ".element-that-dont-exists" == element_list.query
        element_list.first

    expected_message = 'No elements were found with css ".element-that-dont-exists"'

    assert expected_message == err.value.args[0]


def test_element_list_raises_when_element_first_doesnt_exists_in_element_context(
    browser,
    app_url,
):
    "element list raises exception with right information in element context"
    browser.visit(app_url)
    with pytest.raises(ElementDoesNotExist) as err:
        element_list = browser.find_by_css("#inside").find_by_css(
            ".inner-element-that-dont-exists",
        )
        assert "css" == element_list.find_by
        assert ".inner-element-that-dont-exists" == element_list.query
        element_list.first

    expected_message = 'No elements were found with css ".inner-element-that-dont-exists"'

    assert expected_message == err.value.args[0]
