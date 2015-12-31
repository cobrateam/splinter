# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class AsyncFinderTests(object):

    def test_find_by_css_should_found_an_async_element(self):
        self.browser.find_by_css('.add-async-element').click()
        self.assertEqual(1, len(self.browser.find_by_css('.async-element')))

    def test_find_by_xpath_should_found_an_async_element(self):
        self.browser.find_by_css('.add-async-element').click()
        self.assertEqual(1, len(self.browser.find_by_xpath('//h4')))

    def test_find_by_tag_should_found_an_async_element(self):
        self.browser.find_by_css('.add-async-element').click()
        self.assertEqual(1, len(self.browser.find_by_tag('h4')))

    def test_find_by_id_should_found_an_async_element(self):
        self.browser.find_by_css('.add-async-element').click()
        self.assertEqual(1, len(self.browser.find_by_id('async-header')))

    def test_find_by_name_should_found_an_async_element(self):
        self.browser.find_by_css('.add-async-element').click()
        self.assertEqual(1, len(self.browser.find_by_name('async-input')))

    def test_find_by_value_should_found_an_async_element(self):
        self.browser.find_by_css('.add-async-element').click()
        self.assertEqual(1, len(self.browser.find_by_value('async-header-value')))
