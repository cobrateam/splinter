# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from .fake_webapp import EXAMPLE_APP


class MouseInteractionTest(object):
    def test_mouse_over(self):
        "Should be able to perform a mouse over on an element"
        self.browser.visit(EXAMPLE_APP)
        self.browser.find_by_css(".add-element-mouseover").mouse_over()
        self.assertTrue(self.browser.is_element_present_by_id("what-is-your-name"))
        self.browser.find_by_css(".add-element-mouseover").mouse_out()

    def test_mouse_out(self):
        "Should be able to perform a mouse out on an element"
        self.browser.visit(EXAMPLE_APP)
        element = self.browser.find_by_css(".add-element-mouseover")
        element.mouse_over()
        element.mouse_out()
        self.assertTrue(self.browser.is_element_not_present_by_id("what-is-your-name"))

    def test_mouse_out_top_left(self):
        """Should be able to perform a mouse out on an element,
        even if the element is at the top left corner of the screen.
        """
        self.browser.visit(EXAMPLE_APP + '/mouse')
        element = self.browser.find_by_css(".add-element-mouseover")
        element.mouse_over()
        element.mouse_out()
        self.assertTrue(self.browser.is_element_not_present_by_id("what-is-your-name"))

    def test_double_click(self):
        "double click should shows a hidden element"
        self.browser.visit(EXAMPLE_APP)
        button = self.browser.find_by_css(".db-button")
        button.double_click()
        element = self.browser.find_by_css(".should-be-visible-after-double-click")
        self.assertTrue(element.visible)
        self.assertTrue(self.browser.is_element_not_present_by_id("what-is-your-name"))

    def test_right_click(self):
        "should be able to perform a right click on an element"
        self.browser.visit(EXAMPLE_APP)
        element = self.browser.find_by_css(".right-clicable")
        element.right_click()
        self.assertEqual(
            self.browser.find_by_css(".right-clicable").text, "right clicked"
        )

    def test_drag_and_drop(self):
        """
        should be able to perform a drag an element and drop in another element
        """
        droppable = self.browser.find_by_css(".droppable")
        draggable = self.browser.find_by_css(".draggable")
        draggable.drag_and_drop(droppable)
        self.assertEqual(self.browser.find_by_css(".dragged").text, "yes")
