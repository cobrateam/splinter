# -*- coding: utf-8 -*-

# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class IsElementVisibleTest(object):

    def test_is_element_visible_by_css(self):
        "should is element visible by css verify if element is visible"
        self.browser.find_by_css('.show-invisible-element').click()
        self.assertTrue(self.browser.is_element_visible_by_css('#invisible'))

    def test_is_element_visible_by_css_using_a_custom_wait_time(self):
        "should is element visible by css verify if element is visible using a custom wait time"
        self.browser.find_by_css('.show-invisible-element').click()
        self.assertTrue(self.browser.is_element_visible_by_css('#invisible', wait_time=3))

    def test_is_element_visible_by_css_returns_false_if_element_is_not_visible(self):
        "should is element visible by css returns False if element is not visible"
        self.assertFalse(self.browser.is_element_visible_by_css('#invisible'))

    def test_is_element_not_visible_by_css(self):
        "should is element not visible by css verify if element is not visible"
        self.assertTrue(self.browser.is_element_not_visible_by_css('#invisible'))

    def test_is_element_not_visible_by_css_returns_false_if_element_is_visible(self):
        "should is element not visible by css returns False if element is visible"
        self.browser.find_by_css('.show-invisible-element').first.click()
        self.assertFalse(self.browser.is_element_not_visible_by_css('#invisible'))

    def test_is_element_not_visible_by_css_using_a_custom_wait_time(self):
        "should is element not visible by css verify if element is not visible using a custom wait time"
        self.assertTrue(self.browser.is_element_not_visible_by_css('#invisible', wait_time=3))

    def test_is_element_visible_by_xpath(self):
        "should is element visible by xpath verify if element is visible"
        self.browser.find_by_css('.show-invisible-element').click()
        self.assertTrue(self.browser.is_element_visible_by_xpath('//div[@id="invisible"]'))

    def test_is_element_visible_by_xpath_using_a_custom_wait_time(self):
        "should is element visible by xpath verify if element is visible using a custom wait time"
        self.browser.find_by_css('.show-invisible-element').click()
        self.assertTrue(self.browser.is_element_visible_by_xpath('//div[@id="invisible"]', wait_time=3))

    def test_is_element_visible_by_xpath_returns_false_if_element_is_not_visible(self):
        "should is element visible by xpath returns false if element is not visible"
        self.assertFalse(self.browser.is_element_visible_by_xpath('//div[@id="invisible"]'))

    def test_is_element_not_visible_by_xpath(self):
        "should is element not visible by xpath verify if element is not visible"
        self.assertTrue(self.browser.is_element_not_visible_by_xpath('//div[@id="invisible"]'))

    def test_is_element_not_visible_by_xpath_returns_false_if_element_is_visible(self):
        "should is element not visible by xpath returns false if element is visible"
        self.browser.find_by_css('.show-invisible-element').click()
        self.assertFalse(self.browser.is_element_not_visible_by_xpath('//div[@id="invisible"]'))

    def test_is_element_not_visible_by_xpath_using_a_custom_wait_time(self):
        "should is element not visible by xpath verify if element is not visible using a custom wait time"
        self.assertTrue(self.browser.is_element_not_visible_by_xpath('//div[@id="invisible"]', wait_time=3))
