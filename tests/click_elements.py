# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class ClickElementsTest(object):

    def test_click_links(self):
        "should allow to click links"
        self.browser.find_link_by_text('FOO').click()
        assert 'BAR!' in self.browser.html

    def test_click_element_by_css_selector(self):
        "should allow to click at elements by css selector"
        self.browser.find_by_css('a[href="http://localhost:5000/foo"]').click()
        assert 'BAR!' in self.browser.html

    def test_click_input_by_css_selector(self):
        "should allow to click at inputs by css selector"
        self.browser.find_by_css('input[name="send"]').click()
        assert 'My name is: Master Splinter' in self.browser.html

    def test_click_link_by_href(self):
        "should allow to click link by href"
        self.browser.click_link_by_href('http://localhost:5000/foo')
        assert "BAR!" in self.browser.html

    def test_click_link_by_partial_href(self):
        "should allow to click link by partial href"
        self.browser.click_link_by_partial_href('5000/foo')
        assert "BAR!" in self.browser.html

    def test_click_link_by_text(self):
        "should allow to click link by text"
        self.browser.click_link_by_text('FOO')
        assert "BAR!" in self.browser.html

    def test_click_link_by_partial_text(self):
        "should allow to click link by partial text"
        self.browser.click_link_by_partial_text("wordier")
        assert "BAR!" in self.browser.html
