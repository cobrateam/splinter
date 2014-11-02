# -*- coding: utf-8 -*-

# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import tempfile


class ScreenshotTest(object):

    def test_take_screenshot(self):
        "should take a screenshot of the current page"
        filename = self.browser.screenshot()
        self.assertTrue(tempfile.gettempdir() in filename)

    def test_take_screenshot_with_prefix(self):
        "should add the prefix to the screenshot file name"
        filename = self.browser.screenshot(name='foobar')
        self.assertTrue('foobar' in filename)

    def test_take_screenshot_with_suffix(self):
        "should add the suffix to the screenshot file name"
        filename = self.browser.screenshot(suffix='jpeg')
        self.assertEqual('jpeg', filename[-4:])
