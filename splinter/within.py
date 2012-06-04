# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


class Within(object):

    def __init__(self, within_selector):
        self.within_selector = within_selector

    def find_by_css(self, element):
        """
        Performs a find in the element context using the provided selector.
        """
        for context_elements in self.within_selector:
            final_elements = context_elements.find_by_css(element)
        return final_elements

    def find_by_xpath(self, element):
        """
        Performs a find in the element context using the provided selector.
        """
        for context_elements in self.within_selector:
            final_elements = context_elements.find_by_xpath(element)
        return final_elements
