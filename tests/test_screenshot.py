# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os
import tempfile

import pytest
from selenium.common.exceptions import WebDriverException

from .base import supported_browsers
from .fake_webapp import EXAMPLE_APP


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_screenshot_no_unique_file(browser_name, get_new_browser):
    """When the unique_file parameter is false,
    Then the screenshot filename should match the name parameter exactly.
    """
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.screenshot(name="test_screenshot", unique_file=False)
    expected_filepath = os.path.abspath("test_screenshot.png")
    assert os.path.isfile(expected_filepath)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_screenshot(browser_name, get_new_browser):
    """Should take a screenshot of the current page"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    filename = browser.screenshot()
    assert tempfile.gettempdir() in filename


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_screenshot_full_screen(browser_name, get_new_browser):
    """Should take a full screen screenshot of the current page"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    filename = browser.screenshot(full=True)
    assert tempfile.gettempdir() in filename


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_screenshot_with_prefix(browser_name, get_new_browser):
    """Should add the prefix to the screenshot file name"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    filename = browser.screenshot(name="foobar")
    assert "foobar" in filename


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_screenshot_with_suffix(browser_name, get_new_browser):
    """Should add the suffix to the screenshot file name"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    filename = browser.screenshot(suffix=".png")
    assert ".jpg" in filename[-4:]


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_element_screenshot(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_tag("body")
    filename = elem.screenshot()
    assert tempfile.gettempdir() in filename


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_element_screenshot_with_prefix(browser_name, get_new_browser):
    """Should add the prefix to the screenshot file name"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_tag("body")
    filename = elem.screenshot(name="foobar")
    assert "foobar" in filename


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_element_screenshot_full_screen(browser_name, get_new_browser):
    """Should resize the window before taking screenshot of the element"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_tag("body")
    filename = elem.screenshot(name="foobar", full=True)
    assert tempfile.gettempdir() in filename


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_take_nested_element_screenshot(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_tag("body").find_by_css("h1")
    filename = elem.screenshot()
    assert tempfile.gettempdir() in filename


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_element_screenshot_zero_size(browser_name, get_new_browser):
    """Elements with 0 width and 0 height should crash."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_id("zerodiv")

    with pytest.raises(WebDriverException):
        elem.screenshot()
