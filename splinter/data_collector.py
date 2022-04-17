# -*- coding: utf-8 -*-:

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import time
import random
import re


class DataCollector:
    def __init__(self, start_url, browser):
        self.browser = browser
        self.browser.visit(start_url)
        self.data_collection = {}
        self.url_templates = []

    def wait_until_url(self, url):
        while self.browser.url != url:
            time.sleep(5)

    def add_to_data_collection(self, data_label, values):
        if data_label not in self.data_collection:
            self.data_collection[data_label] = []
        self.data_collection[data_label].append(values)

    def remove_html(self, html):
        return re.sub(re.compile("<.*?>"),'', html)

    def _get_innermost_tag_text_containing_strings(self, tag, strings=[]):
        '''
        This method searches for the given tag in a non greedy way, containing
        all the strings in the same order they occur in the input list.
        
        Parameters
        ----------
        tag : STRING
            The tag name (with no angle parenthesis). Case sensitive.
        strings : LIST, optional
            List of strings which must be included after "<tag.." in the same
            order they occur.
            The default is [].

        Returns
        -------
        STRING
            Text inside the matched string after deleting all contained HTML tags.         

        '''
        match = None    
        while match is None:
            match = re.search("<"+tag+"(?:(?!<"+tag+").)*"+".*?".join(strings)+".*?</"+tag+">", self.browser.html)
        return self.remove_html(match.group(0))

    def iterate_over_pages(self, var_name, var_values, callbacks):
        for url_template in self.url_templates:
            placeholder = "{"+var_name+"}"
            if placeholder in url_template:
                for var_value in var_values:
                    self.browser.visit(url_template.replace(placeholder, var_value))
                    for callback, params in callbacks:
                        data = getattr(self, callback)(**params)
                        if data is not None:
                            self.add_to_data_collection(placeholder+"="+var_value, data)

    def wait_random_time(self, min_time, max_time):
        time.sleep(random.randint(min_time,max_time))

    def add_url_template(self, url):
        self.url_templates.append(url)
