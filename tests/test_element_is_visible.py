# Copyright 2022 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from .base import supported_browsers
from .fake_webapp import EXAMPLE_APP


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_element_is_visible(browser_name, get_new_browser):
    """WebDriverElement.is_visible() should verify if element is visible."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".show-invisible-element").click()
    assert browser.find_by_css("#invisible").is_visible()


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_element_is_visible_custom_wait_time(browser_name, get_new_browser):
    """WebDriverElement.is_visible()'s wait_time argument should be respected."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".show-invisible-element").click()
    assert browser.find_by_css("#invisible").is_visible(wait_time=3)


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_element_is_visible_return_false(browser_name, get_new_browser):
    """WebDriverElement.is_visible() should return False if element is not visible."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.find_by_css("#invisible").is_visible()


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_element_is_not_visible(browser_name, get_new_browser):
    """WebDriverElement.is_not_visible() should verify if element is not visible."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.find_by_css("#invisible").is_not_visible()


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_element_is_not_visible_return_false(browser_name, get_new_browser):
    """WebDriverElement.is_not_visible() should return False if element is visible."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".show-invisible-element").click()
    assert not browser.find_by_css("#invisible").is_not_visible()


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_element_is_not_visible_custom_wait_time(browser_name, get_new_browser):
    """WebDriverElement.is_not_visible()'s wait_time argument should be respected."""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.find_by_css("#invisible").is_not_visible(wait_time=3)
