# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class WithinTest(object):

    def test_within_works_right(self):
        "should perform the find only inside the context"
        self.assertFalse(self.browser.find_by_css('h1').is_empty()) #make sure there's a h1
        self.assertTrue(self.browser.within('h1').find_by_css('body').is_empty())

    def test_find_by_css(self):
        "should find by css using context"
        elements = self.browser.within('body').find_by_css('h1')
        self.assertFalse(elements.is_empty())

    def test_find_by_xpath(self):
        "should find by xpath using context"
        xpath_elements = self.browser.within('body').find_by_xpath('//h1')
        css_elements = self.browser.within('body').find_by_css('h1')
        self.assertTrue(css_elements[0].value == xpath_elements[0].value)

