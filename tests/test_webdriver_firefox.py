# -*- coding: utf-8 -*-
import os
import unittest

from nose.tools import raises
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests


class FirefoxBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('firefox')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').first.click()

        html = self.browser.html
        assert 'text/plain' in html
        assert open(file_path).read() in html

    @raises(NotImplementedError)
    def test_mouse_over(self):
        "Firefox should not support mouseover"
        self.browser.find_by_id('visible').first.mouse_over()

    @raises(NotImplementedError)
    def test_mouse_out(self):
        "Firefox should not support mouseout"
        self.browser.find_by_id('visible').first.mouse_out()

    @raises(NotImplementedError)
    def test_double_click(self):
        "Firefox should not support double_click"
        self.browser.find_by_id('visible').double_click()

    @raises(NotImplementedError)
    def test_right_click(self):
        "Firefox should not support right_click"
        self.browser.find_by_id('visible').right_click()

    @raises(NotImplementedError)
    def test_drag_and_drop(self):
        "Firefox should not support drag_and_drop"
        droppable = self.browser.find_by_css('.droppable')
        self.browser.find_by_css('.draggable').drag_and_drop(droppable)

    @raises(NotImplementedError)
    def test_mouseover_should_be_an_alias_to_mouse_over_and_be_deprecated(self):
        "Firefox should not support mouseover"
        self.browser.find_by_id('visible').mouseover()

    @raises(NotImplementedError)
    def test_mouseout_should_be_an_alias_to_mouse_out_and_be_deprecated(self):
        "Firefox should not support mouseout"
        self.browser.find_by_id('visible').mouseout()


class FirefoxWithExtensionTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        extension_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'firebug.xpi')
        cls.browser = Browser(extensions=[extension_path])

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_create_a_firefox_instance_with_extension(self):
        "should be able to load an extension"
        assert 'firebug@software.joehewitt.com' in os.listdir(self.browser.driver.profile.extensionsDir)
