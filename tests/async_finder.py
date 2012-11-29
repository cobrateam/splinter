# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class AsyncFinderTests(object):
    import selenium
    selenium_version = [int(part) for part in selenium.__version__.split('.')]

    def test_find_by_css_should_found_an_async_element(self):
        "should find element by css found an async element"
        self.browser.find_by_css('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_css('.async-element'))

    def test_find_by_xpath_should_found_an_async_element(self):
        "should find by xpath found an async element"
        self.browser.find_by_css('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_xpath('//h4'))

    def test_find_by_tag_should_found_an_async_element(self):
        "should find by tag found an async element"
        self.browser.find_by_css('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_tag('h4'))

    def test_find_by_id_should_found_an_async_element(self):
        "should find by id found an async element"
        self.browser.find_by_css('.add-async-element').first.click()
        if AsyncFinderTests.selenium_version < [2, 27, 0]:
            from time import sleep
            sleep(5)
        assert 1 == len(self.browser.find_by_id('async-header'))

    def test_find_by_name_should_found_an_async_element(self):
        "should find by name found an async element"
        self.browser.find_by_css('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_name('async-input'))

    def test_find_by_value_should_found_an_async_element(self):
        "should find by value found an async element"
        self.browser.find_by_css('.add-async-element').first.click()
        assert 1 == len(self.browser.find_by_value('async-header-value'))
