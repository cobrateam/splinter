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
        assert 'text/plain' in html
        assert open(file_path, 'rb').read().decode('utf-8') in html

    def test_should_support_with_statement(self):
        with Browser('firefox'):
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


@unittest.skipIf(not firefox_installed(), 'firefox is not installed')
class FirefoxBrowserCapabilitiesTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        capabilities = {
            'acceptSslCerts': False,
            'javascriptEnabled': True
        }
        cls.browser = Browser("firefox", capabilities=capabilities)

    def test_capabilities_set(self):
        capabilities = self.browser.driver.capabilities
        self.assertIn('acceptSslCerts', capabilities)
        self.assertEqual(False, capabilities.get('acceptSslCerts'))
        self.assertIn('javascriptEnabled', capabilities)
        self.assertEqual(True, capabilities.get('javascriptEnabled'))

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


@unittest.skipIf(not firefox_installed(), 'firefox is not installed')
class FirefoxBrowserFullScreenTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("firefox", fullscreen=True)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

from contextlib import contextmanager
@contextmanager
def spy_on(an_object, slot_name, spy):
    original_value = getattr(an_object, slot_name)
    setattr(an_object, slot_name, spy)
    try:
        yield spy
    finally:
        setattr(an_object, slot_name, original_value)

class FirefoxCustomPathTest(unittest.TestCase):
    
    def test_custom_path_is_set_correctly(self):
        from splinter.driver.webdriver import firefox
        arguments = {}
        class FakeFox(object):
            def __init__(self, *args, **kwargs):
                arguments['args'] = args
                arguments['kwargs'] = kwargs
        
        sensor = '/some/custom/path'
        
        with spy_on(firefox, 'Firefox', FakeFox):
            browser = Browser('firefox', firefox_binary_path=sensor)
            self.assertEquals(arguments['kwargs']['firefox_binary']._start_cmd, sensor)
    
