# -*- coding: utf-8 -*-

# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import tempfile


class ScreenshotTest(object):
    def test_take_screenshot(self):
        """Should take a screenshot of the current page"""
        filename = self.browser.screenshot()
        assert tempfile.gettempdir() in filename

    def test_take_screenshot_full_screen(self):
        """Should take a full screen screenshot of the current page"""
        filename = self.browser.screenshot(full=True)
        assert tempfile.gettempdir() in filename

    def test_take_screenshot_with_prefix(self):
        """Should add the prefix to the screenshot file name"""
        filename = self.browser.screenshot(name="foobar")
        assert "foobar" in filename

    def test_take_screenshot_with_suffix(self):
        """Should add the suffix to the screenshot file name"""
        filename = self.browser.screenshot(suffix=".jpg")
        assert ".jpg" in filename[-4:]

    def test_take_element_screenshot(self):
        elem = self.browser.find_by_tag("body")
        filename = elem.screenshot()
        assert tempfile.gettempdir() in filename

    def test_take_element_screenshot_with_prefix(self):
        """Should add the prefix to the screenshot file name"""
        elem = self.browser.find_by_tag("body")
        filename = elem.screenshot(name="foobar")
        assert "foobar" in filename

    def test_take_element_screenshot_full_screen(self):
        """Should resize the window before taking screenshot of the element"""
        elem = self.browser.find_by_tag("body")
        filename = elem.screenshot(name="foobar", full=True)
        assert tempfile.gettempdir() in filename

    def test_take_nested_element_screenshot(self):
        elem = self.browser.find_by_tag("body").find_by_css("h1")
        filename = elem.screenshot()
        assert tempfile.gettempdir() in filename
