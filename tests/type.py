# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from fake_webapp import EXAMPLE_APP


class SlowlyTypeTest(object):

    def test_simple_type(self):
        "should provide a away to change field value using type method"
        self.browser.visit(EXAMPLE_APP)
        self.browser.type('query', ' with type method')
        value = self.browser.find_by_name('query').first.value
        self.assertEqual('default value with type method', value)

    def test_simple_type_on_element(self):
        self.browser.visit(EXAMPLE_APP)
        self.browser.find_by_name('query').type(' with type method')
        value = self.browser.find_by_name('query').first.value
        self.assertEqual('default value with type method', value)

    def test_slowly_typing(self):
        "should be able to slowly type some text in a field"
        self.browser.visit(EXAMPLE_APP + 'type')
        num = 0
        num_max = 6
        for key in self.browser.type('type-input', 'typing', slowly=True):
            self.assertEqual(self.browser.is_text_present("#%d" % num), True)
            num += 1
        self.assertEqual(num, num_max)

        element = self.browser.find_by_name('type-input').first
        self.assertEqual(element.value, 'typing')

    def test_slowly_typing_on_element(self):
        self.browser.visit(EXAMPLE_APP + 'type')
        num = 0
        num_max = 6
        for key in self.browser.find_by_name('type-input').type('typing', slowly=True):
            self.assertEqual(self.browser.is_text_present("#%d" % num), True)
            num += 1
        self.assertEqual(num, num_max)

        element = self.browser.find_by_name('type-input').first
        self.assertEqual(element.value, 'typing')
