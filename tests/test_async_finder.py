# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from .base import supported_browsers
from .fake_webapp import EXAMPLE_APP


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_find_by_css_should_found_an_async_element(get_new_browser, browser_name):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".add-async-element").click()
    elements = browser.find_by_css(".async-element", wait_time=30)

    assert 1 == len(elements)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_find_by_xpath_should_found_an_async_element(get_new_browser, browser_name):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".add-async-element").click()
    elements = browser.find_by_xpath("//h4", wait_time=30)

    assert 1 == len(elements)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_find_by_tag_should_found_an_async_element(get_new_browser, browser_name):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".add-async-element").click()
    elements = browser.find_by_tag("h4", wait_time=30)

    assert 1 == len(elements)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_find_by_id_should_found_an_async_element(get_new_browser, browser_name):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".add-async-element").click()
    elements = browser.find_by_id("async-header", wait_time=30)

    assert 1 == len(elements)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_find_by_name_should_found_an_async_element(get_new_browser, browser_name):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".add-async-element").click()
    elements = browser.find_by_name("async-input", wait_time=10)

    assert 1 == len(elements)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_find_by_value_should_found_an_async_element(get_new_browser, browser_name):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".add-async-element").click()
    elements = browser.find_by_value("async-header-value", wait_time=30)

    assert 1 == len(elements)
