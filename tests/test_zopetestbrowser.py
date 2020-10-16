# -*- coding: utf-8 -*-

# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

import six

import pytest

from splinter import Browser
from .base import BaseBrowserTests
from .fake_webapp import EXAMPLE_APP
from .is_element_present_nojs import IsElementPresentNoJSTest


class ZopeTestBrowserDriverTest(
    BaseBrowserTests, IsElementPresentNoJSTest, unittest.TestCase
):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("zope.testbrowser", wait_time=0.1)

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_should_support_with_statement(self):
        with Browser("zope.testbrowser"):
            pass

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "mockfile.txt"
        )
        self.browser.attach_file("file", file_path)
        self.browser.find_by_name("upload").click()

        html = self.browser.html

        assert "text/plain" in html

        with open(file_path) as f:
            assert f.read() in html

    def test_forward_to_none_page(self):
        "should not fail when trying to forward to none"
        browser = Browser("zope.testbrowser")
        browser.visit(EXAMPLE_APP)
        browser.forward()
        self.assertEqual(EXAMPLE_APP, browser.url)
        browser.quit()

    def test_cant_switch_to_frame(self):
        "zope.testbrowser should not be able to switch to frames"
        with self.assertRaises(NotImplementedError) as cm:
            self.browser.get_iframe("frame_123")
            self.fail()

        e = cm.exception
        self.assertEqual("zope.testbrowser doesn't support frames.", e.args[0])

    def test_simple_type(self):
        """
        zope.testbrowser won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type("query", "with type method")

    def test_simple_type_on_element(self):
        """
        zope.testbrowser won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("query").type("with type method")

    def test_can_clear_password_field_content(self):
        "zope.testbrowser should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("password").first.clear()

    def test_can_clear_tel_field_content(self):
        "zope.testbrowser should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("telephone").first.clear()

    def test_can_clear_text_field_content(self):
        "zope.testbrowser should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("query").first.clear()

    def test_can_clear_textarea_content(self):
        "flask should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("description").first.clear()

    def test_can_clear_search_content(self):
        "flask should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("search_keyword").first.clear()

    def test_can_clear_url_content(self):
        "flask should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("url_input").first.clear()

    def test_slowly_typing(self):
        """
        zope.testbrowser won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type("query", "with type method", slowly=True)

    def test_slowly_typing_on_element(self):
        """
        zope.testbrowser won't support type method
        on element because it doesn't interac with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            query = self.browser.find_by_name("query")
            query.type("with type method", slowly=True)

    def test_cant_mouseover(self):
        "zope.testbrowser should not be able to put the mouse over the element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css("#visible").mouse_over()

    def test_cant_mouseout(self):
        "zope.testbrowser should not be able to mouse out of an element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css("#visible").mouse_out()

    def test_links_with_nested_tags_xpath(self):
        links = self.browser.find_by_xpath('//a/span[text()="first bar"]/..')
        self.assertEqual(
            len(links),
            1,
            'Found not exactly one link with a span with text "BAR ONE". %s'
            % (map(lambda item: item.outer_html, links)),
        )

    def test_finding_all_links_by_non_ascii_text(self):
        "should find links by non ascii text"
        non_ascii_encodings = {
            "pangram_pl": u"Jeżu klątw, spłódź Finom część gry hańb!",
            "pangram_ja": u"天 地 星 空",
            "pangram_ru": u"В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!",
            "pangram_eo": u"Laŭ Ludoviko Zamenhof bongustas freŝa ĉeĥa manĝaĵo kun spicoj.",
        }
        for key, text in six.iteritems(non_ascii_encodings):
            link = self.browser.find_link_by_text(text)
            self.assertEqual(key, link["id"])

    def test_fill_form_missing_values(self):
        """Missing values should raise an error."""
        with pytest.raises(NotImplementedError):
            self.browser.fill_form(
                {"query": "new query", "missing_form": "doesn't exist"},
            )
