# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from .fake_webapp import EXAMPLE_APP

class ClickElementsTest:
    def test_click_links(self):
        self.browser.links.find_by_text("FOO").click()
        self.assertIn("BAR!", self.browser.html)

    def test_click_element_by_css_selector(self):
        self.browser.find_by_css('a[href="http://localhost:5000/foo"]').click()
        self.assertIn("BAR!", self.browser.html)
        self.browser.visit(EXAMPLE_APP)

    def test_click_input_by_css_selector(self):
        self.browser.find_by_css('input[name="send"]').click()
        self.assertIn("My name is: Master Splinter", self.browser.html)
        self.browser.visit(EXAMPLE_APP)
