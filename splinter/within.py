# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from element_list import ElementList


class Within(object):

    def __init__(self, context_elements):
        self.context_elements = context_elements

    def find_by_css(self, finder):
        """Performs a find in the element context using the provided css selector"""
        final_elements = ElementList([])
        for context_element in self.context_elements:
            for element in context_element.find_by_css(finder):
                final_elements.append(element)
        return final_elements

    def find_by_xpath(self, finder):
        """Performs a find in the element context using the provided xpath selector"""
        final_elements = ElementList([])
        for context_element in self.context_elements:
            for element in context_element.find_by_xpath(finder):
                final_elements.append(element)
        return final_elements

