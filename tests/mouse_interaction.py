# -*- coding: utf-8 -*-
from fake_webapp import EXAMPLE_APP

class MouseInteractionTest(object):

    def test_mouse_over(self):
        "Should be able to perform a mouse over on an element"
        self.browser.visit(EXAMPLE_APP)
        self.browser.find_by_css(".add-element-mouseover").first.mouseover()
        assert self.browser.is_element_present_by_id('what-is-your-name')

    def test_mouse_out(self):
        "Should be able to perform a mouse out on an element"
        self.browser.visit(EXAMPLE_APP)
        element = self.browser.find_by_css(".add-element-mouseover").first
        element.mouseover()
        element.mouseout()
        assert self.browser.is_element_not_present_by_id('what-is-your-name')
