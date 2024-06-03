# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class ClickElementsTest:
    def test_click_links(self):
        self.browser.links.find_by_text("FOO").click()
        assert "BAR!" in self.browser.html

    def test_click_element_by_css_selector(self):
        self.browser.find_by_css('a[href="http://localhost:5000/foo"]').click()
        assert "BAR!" in self.browser.html

    def test_click_input_by_css_selector(self):
        self.browser.find_by_css('input[name="send"]').click()
        assert "My name is: Master Splinter" in self.browser.html
