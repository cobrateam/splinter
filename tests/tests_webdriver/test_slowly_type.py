# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os

import pytest


xfail_if_safari = pytest.mark.xfail(
    os.getenv("SAFARI"),
    reason="Typing issues with safari need to be investigated.",
)


@xfail_if_safari
def test_simple_type(browser, app_url):
    """should provide a away to change field value using type method"""
    browser.visit(app_url)
    elem = browser.find_by_name("query")
    elem.type(" with type method")
    assert "default value with type method" == elem.value

    browser.find_by_name("description").type("type into textarea")
    value = browser.find_by_name("description").value
    assert "type into textarea" == value


@xfail_if_safari
def test_simple_type_on_element(browser, app_url):
    browser.visit(app_url)
    elem = browser.find_by_name("query")
    elem.type(" with type method")
    assert "default value with type method" == elem.value

    browser.find_by_name("description").type("type into textarea")
    value = browser.find_by_name("description").value
    assert "type into textarea" == value


def test_slowly_typing(browser, app_url):
    """should be able to slowly type some text in a field"""
    for name in ["type-input", "type-textarea"]:
        browser.visit(app_url + "type")
        num = 0
        num_max = 6
        for key in browser.find_by_name(name).type("typing", slowly=True):
            assert browser.is_text_present("#%d" % num)
            num += 1
        assert num == num_max

        element = browser.find_by_name(name)
        assert element.value == "typing"


def test_slowly_typing_on_element(browser, app_url):
    for name in ["type-input", "type-textarea"]:
        browser.visit(app_url + "type")
        num = 0
        num_max = 6
        text_input = browser.find_by_name(name)
        typing = text_input.type("typing", slowly=True)
        for key in typing:
            assert browser.is_text_present("#%d" % num)
            num += 1
        assert num == num_max

        element = browser.find_by_name(name)
        assert element.value == "typing"
