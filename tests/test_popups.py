# -*- coding: utf-8 -*-

# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import platform

from .base import get_browser
from .fake_webapp import EXAMPLE_APP

import pytest


supported_browsers = [
    'chrome', 'firefox', 'chrome_fullscreen', 'firefox_fullscreen',
]

if platform.system() == 'Windows':
    supported_browsers = ['edge']


@pytest.fixture
def get_new_browser(request):
    def new_browser(browser_name):
        browser = get_browser(browser_name)
        request.addfinalizer(browser.quit)
        return browser
    return new_browser


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_lists_all_windows_as_window_instances(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    assert 2 == len(browser.windows)

    for window, handle in zip(
        browser.windows, browser.driver.window_handles
    ):
        assert window.name == handle


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_current_is_a_window_instance_pointing_to_current_window(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.windows.current.name == browser.driver.current_window_handle


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_set_current_to_window_instance_sets_current_window(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    last_current_window = browser.windows.current
    browser.windows.current = browser.windows.current.next
    assert browser.windows.current != last_current_window


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_next_prev_return_next_prev_windows(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    assert browser.windows.current.next == browser.windows.current.prev
    assert browser.windows.current != browser.windows.current.next


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_is_current_returns_true_if_current_window_else_false(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    assert browser.windows.current.is_current
    assert not browser.windows.current.next.is_current

    # Close popup window
    browser.windows.current.close_others()


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_set_is_current_to_true_sets_window_to_current(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    next_window = browser.windows.current.next
    assert not next_window.is_current
    next_window.is_current = True
    assert browser.windows.current == next_window
    assert next_window.is_current


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_get_window_by_index(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    assert browser.windows[0].name == browser.driver.window_handles[0]


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_get_window_by_name(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    window_handle = browser.driver.window_handles[0]
    assert browser.windows[window_handle].name == window_handle


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_close_closes_window(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    current = browser.windows.current
    current.next.close()
    assert 1 == len(browser.windows)
    assert browser.windows.current == current


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_close_current_window_expect_previous_window_becomes_current(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)
    browser.find_by_id("open-popup").click()

    prev = browser.windows.current
    current = prev.next
    prev.next.is_current = True
    current.close()
    assert 1 == len(browser.windows)
    assert browser.windows.current == prev


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_close_others_expect_close_all_other_open_windows(browser_name, get_new_browser):
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    current = browser.windows.current
    browser.find_by_id("open-popup").click()
    current.close_others()

    assert browser.windows[0] == current
    assert 1 == len(browser.windows)
