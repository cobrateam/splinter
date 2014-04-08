# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

class PopupWindowsTest(object):
    def test_lists_all_windows_as_window_instances(self):
        self.browser.find_by_id("open-popup").click()
        self.assertEqual(len(self.browser.windows), 2)
        for window, handle in zip(self.browser.windows, self.browser.driver.window_handles):
            self.assertEqual(window.name, handle)

    def test_active_is_a_window_instance_pointing_to_active_window(self):
        self.assertEqual(self.browser.windows.active.name, self.browser.driver.current_window_handle)

    def test_switch_to_window_expect_sets_current_window(self):
        last_current_window = self.browser.windows.active
        self.browser.switch_to_window(self.browser.windows.active.next)
        self.assertNotEqual(self.browser.windows.active, last_current_window)

    def test_next_prev_return_next_prev_windows(self):
        self.browser.find_by_id("open-popup").click()
        self.assertEqual(self.browser.windows.active.next, self.browser.windows.active.prev)
        self.assertNotEqual(self.browser.windows.active, self.browser.windows.active.next)

    def test_is_active_returns_true_if_active_window_else_false(self):
        self.browser.find_by_id("open-popup").click()
        self.assertTrue(self.browser.windows.active.is_active)
        self.assertFalse(self.browser.windows.active.next.is_active)

    def test_window_activate_sets_window_to_active(self):
        self.browser.find_by_id("open-popup").click()
        next_window = self.browser.windows.active.next
        self.assertFalse(next_window.is_active)
        next_window.activate()
        self.assertEqual(self.browser.windows.active, next_window)
        self.assertTrue(next_window.is_active)

    def test_get_window_by_index(self):
        self.browser.find_by_id("open-popup").click()
        self.assertEqual(self.browser.windows[0].name, self.browser.driver.window_handles[0])

    def test_get_window_by_name(self):
        self.browser.find_by_id("open-popup").click()
        window_handle = self.browser.driver.window_handles[0]
        self.assertEqual(self.browser.windows[window_handle].name, window_handle)

    def test_close_closes_window(self):
        self.browser.find_by_id("open-popup").click()
        current = self.browser.windows.active
        current.next.close()
        self.assertEqual(len(self.browser.windows), 1)
        self.assertEqual(self.browser.windows.active, current)

    def test_close_active_window_expect_previous_window_becomes_current(self):
        self.browser.find_by_id("open-popup").click()
        prev = self.browser.windows.active
        current = prev.next
        prev.next.activate()
        current.close()
        self.assertEqual(len(self.browser.windows), 1)
        self.assertEqual(self.browser.windows.active, prev)

    def test_close_others_expect_close_all_other_open_windows(self):
        current = self.browser.windows.active
        self.browser.find_by_id("open-popup").click()
        current.close_others()
        self.assertEqual(self.browser.windows[0], current)
        self.assertEqual(len(self.browser.windows), 1)
