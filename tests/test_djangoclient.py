# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os
import sys
import time
import unittest

import django
import pytest

from .base import BaseBrowserTests
from .base import get_browser
from .fake_webapp import EXAMPLE_APP
from splinter import Browser


sys.path.append("tests/fake_django")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"


django.setup()


class DjangoClientDriverTest(BaseBrowserTests, unittest.TestCase):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = get_browser("django")
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self):
        self.browser.visit(EXAMPLE_APP)

    def test_should_support_with_statement(self):
        with Browser("django") as internet:
            self.assertIsNotNone(internet)

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "mockfile.txt",
        )
        self.browser.attach_file("file", file_path)
        self.browser.find_by_name("upload").click()

        html = self.browser.html
        self.assertIn("text/plain", html)
        self.assertIn(open(file_path).read(), html)

    def test_forward_to_none_page(self):
        "should not fail when trying to forward to none"
        browser = Browser("django")
        browser.visit(EXAMPLE_APP)
        browser.forward()
        self.assertEqual(EXAMPLE_APP, browser.url)
        browser.quit()

    def test_can_clear_password_field_content(self):
        "django should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("password").first.clear()

    def test_can_clear_tel_field_content(self):
        "django should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("telephone").first.clear()

    def test_can_clear_text_field_content(self):
        "django should not be able to clear"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("query").first.clear()

    def test_cant_switch_to_frame(self):
        "django driver should not be able to switch to frames"
        with self.assertRaises(NotImplementedError) as cm:
            self.browser.get_iframe("frame_123")
            self.fail()

        e = cm.exception
        self.assertEqual("django doesn't support frames.", e.args[0])

    def test_simple_type(self):
        """
        django won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type("query", "with type method")

    def test_simple_type_on_element(self):
        """
        django won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_name("query").type("with type method")

    def test_slowly_typing(self):
        """
        django won't support type method
        because it doesn't interact with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            self.browser.type("query", "with type method", slowly=True)

    def test_slowly_typing_on_element(self):
        """
        django won't support type method
        on element because it doesn't interac with JavaScript
        """
        with self.assertRaises(NotImplementedError):
            query = self.browser.find_by_name("query")
            query.type("with type method", slowly=True)

    def test_cant_mouseover(self):
        "django should not be able to put the mouse over the element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css("#visible").mouse_over()

    def test_cant_mouseout(self):
        "django should not be able to mouse out of an element"
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_css("#visible").mouse_out()

    def test_links_with_nested_tags_xpath(self):
        links = self.browser.find_by_xpath('//a/span[text()="first bar"]/..')
        self.assertEqual(
            len(links),
            1,
            'Found not exactly one link with a span with text "BAR ONE". %s'
            % [item.outer_html for item in links],
        )

    def test_finding_all_links_by_non_ascii_text(self):
        "should find links by non ascii text"
        non_ascii_encodings = {
            "pangram_pl": "Jeżu klątw, spłódź Finom część gry hańb!",
            "pangram_ja": "天 地 星 空",
            "pangram_ru": "В чащах юга жил бы цитрус? Да, но фальшивый экземпляр!",
            "pangram_eo": "Laŭ Ludoviko Zamenhof bongustas freŝa ĉeĥa manĝaĵo kun spicoj.",
        }
        for key, text in non_ascii_encodings.items():
            link = self.browser.links.find_by_text(text)
            self.assertEqual(key, link["id"])

    def test_cookies_extra_parameters(self):
        """Cookie can be created with extra parameters."""
        timestamp = int(time.time() + 120)
        self.browser.cookies.add({"sha": "zam"}, expires=timestamp)
        cookie = self.browser._browser.cookies["sha"]
        assert timestamp == cookie["expires"]


class DjangoClientDriverTestWithCustomHeaders(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        custom_headers = {
            "X-Splinter-Customheaders-1": "Hello",
            "X-Splinter-Customheaders-2": "Bye",
        }
        cls.browser = Browser("django", custom_headers=custom_headers)

    def test_create_a_phantomjs_with_custom_headers(self):
        self.browser.visit(EXAMPLE_APP + "headers")
        self.assertTrue(
            self.browser.is_text_present("X-Splinter-Customheaders-1: Hello"),
        )
        self.assertTrue(self.browser.is_text_present("X-Splinter-Customheaders-2: Bye"))

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
