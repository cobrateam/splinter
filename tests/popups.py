# -*- coding: utf-8 -*-

# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class PopupWindowsTest(object):
    def test_lists_all_windows_as_window_instances(self):
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)
        browser.find_by_id("open-popup").click()

        assert 2 == len(browser.windows)

        for window, handle in zip(
            browser.windows, browser.driver.window_handles
        ):
            assert window.name == handle

        browser.quit()

    def test_current_is_a_window_instance_pointing_to_current_window(self):
        assert self.browser.windows.current.name == self.browser.driver.current_window_handle

    def test_set_current_to_window_instance_sets_current_window(self):
        self.browser.find_by_id("open-popup").click()

        last_current_window = self.browser.windows.current
        self.browser.windows.current = self.browser.windows.current.next
        assert self.browser.windows.current != last_current_window

    def test_next_prev_return_next_prev_windows(self):
        browser = self.get_new_browser()
        browser.visit(self.EXAMPLE_APP)
        browser.find_by_id("open-popup").click()

        assert browser.windows.current.next == browser.windows.current.prev
        assert browser.windows.current != browser.windows.current.next

        browser.quit()

    def test_is_current_returns_true_if_current_window_else_false(self):
        self.browser.find_by_id("open-popup").click()

        assert self.browser.windows.current.is_current
        assert not self.browser.windows.current.next.is_current

        # Close popup window
        self.browser.windows.current.close_others()

    def test_set_is_current_to_true_sets_window_to_current(self):
        self.browser.find_by_id("open-popup").click()
        next_window = self.browser.windows.current.next
        assert not next_window.is_current
        next_window.is_current = True
        assert self.browser.windows.current == next_window
        assert next_window.is_current

    def test_get_window_by_index(self):
        self.browser.find_by_id("open-popup").click()
        assert self.browser.windows[0].name == self.browser.driver.window_handles[0]

    def test_get_window_by_name(self):
        self.browser.find_by_id("open-popup").click()
        window_handle = self.browser.driver.window_handles[0]
        assert self.browser.windows[window_handle].name == window_handle

    def test_close_closes_window(self):
        self.browser.find_by_id("open-popup").click()
        current = self.browser.windows.current
        current.next.close()
        assert 1 == len(self.browser.windows)
        assert self.browser.windows.current == current

    def test_close_current_window_expect_previous_window_becomes_current(self):
        self.browser.find_by_id("open-popup").click()
        prev = self.browser.windows.current
        current = prev.next
        prev.next.is_current = True
        current.close()
        assert 1 == len(self.browser.windows)
        assert self.browser.windows.current == prev

    def test_close_others_expect_close_all_other_open_windows(self):
        current = self.browser.windows.current
        self.browser.find_by_id("open-popup").click()
        current.close_others()
        assert self.browser.windows[0] == current
        assert 1 == len(self.browser.windows)
