# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os
import tempfile

import pytest
from selenium.common.exceptions import WebDriverException


def test_take_screenshot_no_unique_file(browser, app_url):
    """When the unique_file parameter is false,
    Then the screenshot filename should match the name parameter exactly.
    """
    browser.visit(app_url)

    browser.screenshot(name="test_screenshot", unique_file=False)
    expected_filepath = os.path.abspath("test_screenshot.png")
    assert os.path.isfile(expected_filepath)


def test_take_screenshot(browser, app_url):
    """Should take a screenshot of the current page"""
    browser.visit(app_url)

    filename = browser.screenshot()
    assert tempfile.gettempdir() in filename


def test_take_screenshot_full_screen(browser, app_url):
    """Should take a full screen screenshot of the current page"""
    browser.visit(app_url)

    filename = browser.screenshot(full=True)
    assert tempfile.gettempdir() in filename


def test_take_screenshot_with_prefix(browser, app_url):
    """Should add the prefix to the screenshot file name"""
    browser.visit(app_url)

    filename = browser.screenshot(name="foobar")
    assert "foobar" in filename


def test_take_screenshot_with_suffix(browser, app_url):
    """Should add the suffix to the screenshot file name"""
    browser.visit(app_url)

    filename = browser.screenshot(suffix=".png")
    assert ".png" in filename[-4:]


def test_take_element_screenshot(browser, app_url):
    browser.visit(app_url)

    elem = browser.find_by_tag("body")
    filename = elem.screenshot()
    assert tempfile.gettempdir() in filename


def test_take_element_screenshot_with_prefix(browser, app_url):
    """Should add the prefix to the screenshot file name"""
    browser.visit(app_url)

    elem = browser.find_by_tag("body")
    filename = elem.screenshot(name="foobar")
    assert "foobar" in filename


def test_take_element_screenshot_full_screen(browser, app_url):
    """Should resize the window before taking screenshot of the element"""
    browser.visit(app_url)

    elem = browser.find_by_tag("body")
    filename = elem.screenshot(name="foobar", full=True)
    assert tempfile.gettempdir() in filename


def test_take_nested_element_screenshot(browser, app_url):
    browser.visit(app_url)

    elem = browser.find_by_tag("body").find_by_css("h1")
    filename = elem.screenshot()
    assert tempfile.gettempdir() in filename


def test_element_screenshot_zero_size(browser, app_url):
    """Elements with 0 width and 0 height should crash."""
    browser.visit(app_url)

    elem = browser.find_by_id("zerodiv")

    with pytest.raises(WebDriverException):
        elem.screenshot()
