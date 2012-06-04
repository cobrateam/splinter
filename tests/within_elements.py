# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class Within(object):

    def test_return_a_list_with_elements(self):
        "should return a single element in list"
        elements = self.browser.within('body').find_by_css('h1')
        assert not elements.is_empty()

    def test_find_by_xpath_with_context(self):
        """should find by xpath using context"""
        xpath_elements = self.browser.within('body').find_by_xpath('//h1')
        css_elements = self.browser.within('body').find_by_css('h1')
        assert css_elements.value == xpath_elements.value
