# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class ClickElementsTest(object):
    def test_click_links(self):
        self.browser.find_link_by_text("FOO").click()
        self.assertIn("BAR!", self.browser.html)

    def test_click_element_by_css_selector(self):
        self.browser.find_by_css('a[href="http://localhost:5000/foo"]').click()
        self.assertIn("BAR!", self.browser.html)

    def test_click_input_by_css_selector(self):
        self.browser.find_by_css('input[name="send"]').click()
        self.assertIn("My name is: Master Splinter", self.browser.html)

    def test_click_link_by_href(self):
        self.browser.click_link_by_href("http://localhost:5000/foo")
        self.assertIn("BAR!", self.browser.html)

    def test_click_link_by_partial_href(self):
        self.browser.click_link_by_partial_href("5000/foo")
        self.assertIn("BAR!", self.browser.html)

    def test_click_link_by_text(self):
        self.browser.click_link_by_text("FOO")
        self.assertIn("BAR!", self.browser.html)

    def test_click_link_by_partial_text(self):
        self.browser.click_link_by_partial_text("wordier")
        self.assertIn("BAR!", self.browser.html)

    def test_click_link_by_id(self):
        self.browser.click_link_by_id("foo")
        self.assertIn("BAR!", self.browser.html)
