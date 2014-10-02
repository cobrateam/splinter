# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

from splinter import Browser
from .fake_webapp import EXAMPLE_APP
from .is_element_visible import IsElementVisibleTest


def firefox_installed():
    try:
        Browser("firefox")
    except OSError:
        return False
    return True


@unittest.skipIf(not firefox_installed(), 'firefox is not installed')
class FirefoxBrowserTest(IsElementVisibleTest, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("firefox")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'mockfile.txt'
        )
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').click()

        html = self.browser.html
        assert b'text/plain' in html
        assert open(file_path).read().encode('utf-8') in html

    def test_should_support_with_statement(self):
        with Browser('firefox') as internet:
            pass