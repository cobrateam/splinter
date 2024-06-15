# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import time


def test_lists_all_windows_as_window_instances(browser, app_url):
    browser.visit(app_url)

    browser.find_by_id("open-popup").click()

    # Wait for popup to open
    windows_count = 0
    timeout = time.time() + 10
    while time.time() <= timeout:
        windows_count = len(browser.windows)
        if 2 == windows_count:
            break

    assert 2 == windows_count

    for window, handle in zip(browser.windows, browser.driver.window_handles):
        assert window.name == handle


def test_current_is_a_window_instance_pointing_to_current_window(browser, app_url):
    browser.visit(app_url)

    assert browser.windows.current.name == browser.driver.current_window_handle


def test_set_current_to_window_instance_sets_current_window(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    last_current_window = browser.windows.current
    browser.windows.current = browser.windows.current.next
    assert browser.windows.current != last_current_window


def test_next_prev_return_next_prev_windows(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    assert browser.windows.current.next == browser.windows.current.prev
    assert browser.windows.current != browser.windows.current.next


def test_is_current_returns_true_if_current_window_else_false(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    assert browser.windows.current.is_current
    assert not browser.windows.current.next.is_current

    # Close popup window
    browser.windows.current.close_others()


def test_set_is_current_to_true_sets_window_to_current(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    next_window = browser.windows.current.next
    assert not next_window.is_current
    next_window.is_current = True
    assert browser.windows.current == next_window
    assert next_window.is_current


def test_get_window_by_index(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    assert browser.windows[0].name == browser.driver.window_handles[0]


def test_get_window_by_name(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    window_handle = browser.driver.window_handles[0]
    assert browser.windows[window_handle].name == window_handle


def test_close_closes_window(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    current = browser.windows.current
    current.next.close()
    assert 1 == len(browser.windows)
    assert browser.windows.current == current


def test_close_current_window_expect_previous_window_becomes_current(browser, app_url):
    browser.visit(app_url)
    browser.find_by_id("open-popup").click()

    prev = browser.windows.current
    current = prev.next
    prev.next.is_current = True
    current.close()
    assert 1 == len(browser.windows)
    assert browser.windows.current == prev


def test_close_others_expect_close_all_other_open_windows(browser, app_url):
    browser.visit(app_url)

    current = browser.windows.current
    browser.find_by_id("open-popup").click()
    current.close_others()

    assert browser.windows[0] == current
    assert 1 == len(browser.windows)
