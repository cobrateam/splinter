# Copyright 2022 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import time

from tests.fake_webapp import EXAMPLE_APP


def test_element_is_visible(browser):
    """WebDriverElement.is_visible() should verify if element is visible."""
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".show-invisible-element").click()
    assert browser.find_by_css("#invisible").is_visible()


def test_element_is_visible_custom_wait_time(browser):
    """WebDriverElement.is_visible()'s wait_time argument should be respected."""
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".show-invisible-element").click()
    assert browser.find_by_css("#invisible").is_visible(wait_time=12)


def test_element_is_visible_return_false(browser):
    """WebDriverElement.is_visible() should return False if element is not visible."""
    browser.visit(EXAMPLE_APP)

    assert not browser.find_by_css("#invisible").is_visible()


def test_element_is_not_visible(browser):
    """WebDriverElement.is_not_visible() should verify if element is not visible."""
    browser.visit(EXAMPLE_APP)

    assert browser.find_by_css("#invisible").is_not_visible()


def test_element_is_not_visible_return_false(browser):
    """WebDriverElement.is_not_visible() should return False if element is visible."""
    browser.visit(EXAMPLE_APP)

    browser.find_by_css(".show-invisible-element").click()
    assert not browser.find_by_css("#invisible").is_not_visible()


def test_element_is_not_visible_custom_wait_time(browser):
    """WebDriverElement.is_not_visible()'s wait_time argument should be respected."""
    browser.visit(EXAMPLE_APP)

    assert browser.find_by_css("#invisible").is_not_visible(wait_time=12)


def test_element_is_visible_element_removed(browser):
    """
    Given an element has been found
    When it is removed from the page
    Then the is_visible() method for this element will return False
    """
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_css("#removed_after_5_seconds")

    # Wait for the element to not be visible
    time.sleep(5.5)

    assert not elem.is_visible()


def test_element_is_not_visible_element_removed(browser):
    """
    Given an element has been found
    When it is removed from the page
    Then the is_not_visible() method for this element will return True
    """
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_css("#removed_after_5_seconds")

    # Wait for the element to not be visible
    time.sleep(5.5)

    assert elem.is_not_visible()
