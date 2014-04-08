# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

from splinter import Browser
from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests


def firefox_installed():
    try:
        Browser("firefox")
    except OSError:
        return False
    return True


@unittest.skipIf(not firefox_installed(), 'firefox is not installed')
class FirefoxBrowserTest(WebDriverTests, unittest.TestCase):
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


@unittest.skipIf(not firefox_installed(), 'firefox is not installed')
class FirefoxWithExtensionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        extension_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'firebug.xpi'
        )
        cls.browser = Browser('firefox', extensions=[extension_path])

    def test_create_a_firefox_instance_with_extension(self):
        "should be able to load an extension"
        self.assertIn(
            'firebug@software.joehewitt.com',
            os.listdir(self.browser.driver.profile.extensionsDir)
        )

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


@unittest.skipIf(not firefox_installed(), 'firefox is not installed')
class FirefoxBrowserProfilePreferencesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        preferences = {
            'dom.max_script_run_time': 360,
            'devtools.inspector.enabled': True,
        }
        cls.browser = Browser("firefox", profile_preferences=preferences)

    def test_preference_set(self):
        preferences = self.browser.driver.profile.default_preferences
        self.assertIn('dom.max_script_run_time', preferences)
        value = preferences.get('dom.max_script_run_time')
        self.assertEqual(int(value), 360)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
