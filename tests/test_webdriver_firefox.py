# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

import pytest

from splinter import Browser
from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests, get_browser


def firefox_installed():
    try:
        Browser("firefox")
    except OSError:
        return False
    return True


class FirefoxBase(object):
    @pytest.fixture(autouse=True, scope='class')
    def teardown(self, request):
        request.addfinalizer(self.browser.quit)


class FirefoxBrowserTest(WebDriverTests, FirefoxBase, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('firefox', fullscreen=False)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "mockfile.txt"
        )
        self.browser.attach_file("file", file_path)
        self.browser.find_by_name("upload").click()

        html = self.browser.html
        self.assertIn("text/plain", html)
        self.assertIn(open(file_path, "rb").read().decode("utf-8"), html)

    def test_should_support_with_statement(self):
        with Browser("firefox"):
            pass


class FirefoxWithExtensionTest(FirefoxBase, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        extension_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "firebug.xpi"
        )

        request.cls.browser = get_browser('firefox', extensions=[extension_path])

    def test_create_a_firefox_instance_with_extension(self):
        "should be able to load an extension"
        self.assertIn(
            "firebug@software.joehewitt.com",
            os.listdir(self.browser.driver.profile.extensionsDir),
        )


class FirefoxBrowserProfilePreferencesTest(FirefoxBase, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        preferences = {
            "dom.max_script_run_time": 360,
            "devtools.inspector.enabled": True,
        }

        request.cls.browser = get_browser('firefox', profile_preferences=preferences)

    def test_preference_set(self):
        preferences = self.browser.driver.profile.default_preferences
        self.assertIn("dom.max_script_run_time", preferences)
        value = preferences.get("dom.max_script_run_time")
        self.assertEqual(int(value), 360)


class FirefoxBrowserCapabilitiesTest(FirefoxBase, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('firefox', capabilities={"pageLoadStrategy": "eager"})

    def test_capabilities_set(self):
        capabilities = self.browser.driver.capabilities
        self.assertIn("pageLoadStrategy", capabilities)
        self.assertEqual("eager", capabilities.get("pageLoadStrategy"))


class FirefoxBrowserFullScreenTest(FirefoxBase, unittest.TestCase):
    @pytest.fixture(autouse=True, scope='class')
    def setup_browser(self, request):
        request.cls.browser = get_browser('firefox', fullscreen=True)
