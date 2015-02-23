# -*- coding: utf-8 -*-

# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class PopupWindowsTest(object):

    def test_lists_all_windows_as_window_instances(self):
        self.browser.find_by_id("open-popup").click()
        self.assertEqual(len(self.browser.windows), 2)
        for window, handle in zip(self.browser.windows, self.browser.driver.window_handles):
            self.assertEqual(window.name, handle)

    def test_current_is_a_window_instance_pointing_to_current_window(self):
        self.assertEqual(self.browser.windows.current.name, self.browser.driver.current_window_handle)

    def test_set_current_to_window_instance_sets_current_window(self):
        last_current_window = self.browser.windows.current
        self.browser.windows.current = self.browser.windows.current.next
        self.assertNotEqual(self.browser.windows.current, last_current_window)

    def test_next_prev_return_next_prev_windows(self):
        self.browser.find_by_id("open-popup").click()
        self.assertEqual(self.browser.windows.current.next, self.browser.windows.current.prev)
        self.assertNotEqual(self.browser.windows.current, self.browser.windows.current.next)

    def test_is_current_returns_true_if_current_window_else_false(self):
        self.browser.find_by_id("open-popup").click()
        self.assertTrue(self.browser.windows.current.is_current)
        self.assertFalse(self.browser.windows.current.next.is_current)

    def test_set_is_current_to_True_sets_window_to_current(self):
        self.browser.find_by_id("open-popup").click()
        next_window = self.browser.windows.current.next
        self.assertFalse(next_window.is_current)
        next_window.is_current = True
        self.assertEqual(self.browser.windows.current, next_window)
        self.assertTrue(next_window.is_current)

    def test_get_window_by_index(self):
        self.browser.find_by_id("open-popup").click()
        self.assertEqual(self.browser.windows[0].name, self.browser.driver.window_handles[0])

    def test_get_window_by_name(self):
        self.browser.find_by_id("open-popup").click()
        window_handle = self.browser.driver.window_handles[0]
        self.assertEqual(self.browser.windows[window_handle].name, window_handle)

    def test_close_closes_window(self):
        self.browser.find_by_id("open-popup").click()
        current = self.browser.windows.current
        current.next.close()
        self.assertEqual(len(self.browser.windows), 1)
        self.assertEqual(self.browser.windows.current, current)

    def test_close_current_window_expect_previous_window_becomes_current(self):
        self.browser.find_by_id("open-popup").click()
        prev = self.browser.windows.current
        current = prev.next
        prev.next.is_current = True
        current.close()
        self.assertEqual(len(self.browser.windows), 1)
        self.assertEqual(self.browser.windows.current, prev)

    def test_close_others_expect_close_all_other_open_windows(self):
        current = self.browser.windows.current
        self.browser.find_by_id("open-popup").click()
        current.close_others()
        self.assertEqual(self.browser.windows[0], current)
        self.assertEqual(len(self.browser.windows), 1)
