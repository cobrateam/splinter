# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class ElementTest(object):

    def test_element_has_class_when_element_has_the_class_as_first_class(self):
        self.assertTrue(self.browser.find_by_css('.has-class-first').has_class('has-class-first'))

    def test_element_has_class_when_element_has_the_class_as_middle_class(self):
        self.assertTrue(self.browser.find_by_css('.has-class-middle').has_class('has-class-middle'))

    def test_element_has_class_when_element_has_the_class_as_end_class(self):
        self.assertTrue(self.browser.find_by_css('.has-class-end').has_class('has-class-end'))

    def test_element_has_class_when_element_doesnt_have_the_class(self):
        self.assertFalse(self.browser.find_by_css('.has-class-first').has_class('has-class'))

    def test_element_outer_html(self):
        self.assertEqual(
            self.browser.find_by_id('html-property').outer_html,
            u'<div id="html-property" class="outer html classes">inner <div class="inner-html">inner text</div> html test</div>'
        )

    def test_element_html(self):
        self.assertEqual(
            self.browser.find_by_id('html-property').html,
            u'inner <div class="inner-html">inner text</div> html test'
        )
