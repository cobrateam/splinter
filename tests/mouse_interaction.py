# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import warnings

from .fake_webapp import EXAMPLE_APP


class MouseInteractionTest(object):

    def test_mouse_over(self):
        "Should be able to perform a mouse over on an element"
        self.browser.visit(EXAMPLE_APP)
        self.browser.find_by_css(".add-element-mouseover").mouse_over()
        assert self.browser.is_element_present_by_id('what-is-your-name')
        self.browser.find_by_css(".add-element-mouseover").mouse_out()

    def test_mouse_out(self):
        "Should be able to perform a mouse out on an element"
        self.browser.visit(EXAMPLE_APP)
        element = self.browser.find_by_css(".add-element-mouseover")
        element.mouse_over()
        element.mouse_out()
        assert not self.browser.is_element_present_by_id('what-is-your-name')

    def test_double_click(self):
        "double click should shows a hidden element"
        self.browser.visit(EXAMPLE_APP)
        button = self.browser.find_by_css(".db-button")
        button.double_click()
        element = self.browser.find_by_css(
            ".should-be-visible-after-double-click"
        )
        assert element.visible
        assert self.browser.is_element_not_present_by_id('what-is-your-name')

    def test_right_click(self):
        "should be able to perform a right click on an element"
        self.browser.visit(EXAMPLE_APP)
        element = self.browser.find_by_css(".right-clicable")
        element.right_click()
        self.assertEqual(
            self.browser.find_by_css('.right-clicable').text,
            'right clicked'
        )

    def test_drag_and_drop(self):
        """
        should be able to perform a drag an element and drop in another element
        """
        droppable = self.browser.find_by_css('.droppable')
        draggable = self.browser.find_by_css('.draggable')
        draggable.drag_and_drop(droppable)
        assert self.browser.find_by_css('.dragged').text == 'yes'

    def test_mouseover_should_be_an_alias_to_mouse_over(self):
        "mouseover should be an alias to mouse_over and be deprecated"
        with warnings.catch_warnings(record=True) as warnings_list:
            self.browser.visit(EXAMPLE_APP)
            warnings.simplefilter("always")
            element = self.browser.find_by_css(".add-element-mouseover")
            element.mouseover()
            warn_message = warnings_list[-1].message
            assert type(warn_message) is DeprecationWarning
            assert 'mouse_over' in warn_message.args[0]

    def test_mouseout_should_be_an_alias_to_mouse_out_and_be_deprecated(self):
        "mouseout should be an alias do mouse_out and be deprecated"
        with warnings.catch_warnings(record=True) as warnings_list:
            self.browser.visit(EXAMPLE_APP)
            warnings.simplefilter("always")
            self.browser.find_by_css(".add-element-mouseover").mouseout()
            warn_message = warnings_list[-1].message
            assert type(warn_message) is DeprecationWarning
            assert 'mouse_out' in warn_message.args[0]
