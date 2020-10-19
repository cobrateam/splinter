#!/usr/bin/env python

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import unittest
from splinter import Browser


class TestGoogleSearch(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_visiting_google_com_returns_a_page_with_google_in_title(self):
        self.browser.visit("http://www.google.com/")
        self.assertIn("Google", self.browser.title)

    def test_filling_splinter_in_the_search_box_returns_splinter_website(self):
        self.browser.visit("http://www.google.com/")
        self.browser.fill("q", "Splinter")
        search_button = self.browser.find_by_name("btnG").first
        while not search_button.visible:
            # waits for the JavaScript to put the button on the page
            pass
        search_button.click()
        self.assertTrue(self.browser.is_text_present("splinter.readthedocs.org"))


unittest.main()
