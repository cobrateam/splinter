# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from __future__ import with_statement

from async_finder import AsyncFinderTests
from click_elements import ClickElementsTest
from cookies import CookiesTest
from element_does_not_exist import ElementDoestNotExistTest
from fake_webapp import EXAMPLE_APP
from find_elements import FindElementsTest
from form_elements import FormElementsTest
from iframes import IFrameElementsTest
from element import ElementTest
from is_element_present import IsElementPresentTest
from is_text_present import IsTextPresentTest
from mouse_interaction import MouseInteractionTest
from status_code import StatusCodeTest
from type import SlowlyTypeTest
from popups import PopupWindowsTest


class BaseBrowserTests(ElementTest, FindElementsTest, FormElementsTest, ClickElementsTest, CookiesTest, SlowlyTypeTest):

    def setUp(self):
        self.fail("You should set up your browser in the setUp() method")

    def test_can_open_page(self):
        "should be able to visit, get title and quit"
        title = self.browser.title
        self.assertEqual('Example Title', title)

    def test_can_back_on_history(self):
        "should be able to back on history"
        self.browser.visit("%s/iframe" % EXAMPLE_APP.rstrip('/'))
        self.browser.back()
        self.assertEqual(EXAMPLE_APP, self.browser.url)

    def test_can_forward_on_history(self):
        "should be able to forward history"
        url = "%s/iframe" % EXAMPLE_APP.rstrip('/')
        self.browser.visit(url)
        self.browser.back()
        self.browser.forward()
        self.assertEqual(url, self.browser.url)

    def test_should_have_html(self):
        "should have access to the html"
        html = self.browser.html
        assert '<title>Example Title</title>' in html
        assert '<h1 id="firstheader">Example Header</h1>' in html

    def test_should_reload_a_page(self):
        "should reload a page"
        title = self.browser.title
        self.browser.reload()
        self.assertEqual('Example Title', title)

    def test_should_have_url(self):
        "should have access to the url"
        self.assertEqual(EXAMPLE_APP, self.browser.url)

    def test_accessing_attributes_of_links(self):
        "should allow link's attributes retrieval"
        foo = self.browser.find_link_by_text('FOO').first
        self.assertEqual('http://localhost:5000/foo', foo['href'])

    def test_accessing_attributes_of_inputs(self):
        "should allow input's attributes retrieval"
        button = self.browser.find_by_css('input[name="send"]').first
        self.assertEqual('send', button['name'])

    def test_accessing_attributes_of_simple_elements(self):
        "should allow simple element's attributes retrieval"
        header = self.browser.find_by_css('h1').first
        self.assertEqual('firstheader', header['id'])

    def test_links_should_have_value_attribute(self):
        foo = self.browser.find_link_by_href('http://localhost:5000/foo').first
        self.assertEqual('FOO', foo.value)

    def test_should_receive_browser_on_parent(self):
        "element should contains the browser on \"parent\" attribute"
        element = self.browser.find_by_id("firstheader").first
        self.assertEqual(self.browser, element.parent)


class WebDriverTests(BaseBrowserTests, IFrameElementsTest, ElementDoestNotExistTest, IsElementPresentTest, AsyncFinderTests, IsTextPresentTest, StatusCodeTest, MouseInteractionTest, PopupWindowsTest):

    def test_can_execute_javascript(self):
        "should be able to execute javascript"
        self.browser.execute_script("$('body').empty()")
        self.assertEqual("", self.browser.find_by_tag("body").first.value)

    def test_can_evaluate_script(self):
        "should evaluate script"
        self.assertEqual(8, self.browser.evaluate_script("4+4"))

    def test_can_see_the_text_for_an_element(self):
        "should provide text for an element"
        self.assertEqual(self.browser.find_by_id("simple_text").first.text, "my test text")

    def test_the_text_for_an_element_strips_html_tags(self):
        "should show that the text attribute strips html"
        self.assertEqual(self.browser.find_by_id("text_with_html").first.text, "another bit of text")

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        self.assertTrue(self.browser.find_by_id("visible").first.visible)

    def test_can_verify_if_a_element_is_invisible(self):
        "should provide verify if element is invisible"
        self.assertFalse(self.browser.find_by_id("invisible").first.visible)

    def test_default_wait_time_should_be_2(self):
        "should driver default wait time 2"
        self.assertEqual(2, self.browser.wait_time)

    def test_access_alerts_and_accept_them(self):
        self.browser.visit(EXAMPLE_APP + 'alert')
        self.browser.find_by_tag('h1').first.click()
        alert = self.browser.get_alert()
        self.assertEqual('This is an alert example.', alert.text)
        alert.accept()

    def test_access_prompts_and_be_able_to_fill_then(self):
        self.browser.visit(EXAMPLE_APP + 'alert')
        self.browser.find_by_tag('h2').first.click()

        alert = self.browser.get_alert()
        self.assertEqual('What is your name?', alert.text)
        alert.fill_with('Splinter')
        alert.accept()

        response = self.browser.get_alert()
        self.assertEqual('Splinter', response.text)
        response.accept()

    def test_access_confirm_and_accept_and_dismiss_them(self):
        self.browser.visit(EXAMPLE_APP + 'alert')

        self.browser.find_by_tag('h3').first.click()
        alert = self.browser.get_alert()

        self.assertEqual('Should I continue?', alert.text)
        alert.accept()
        alert = self.browser.get_alert()
        self.assertEqual('You say I should', alert.text)
        alert.accept()

        self.browser.find_by_tag('h3').first.click()
        alert = self.browser.get_alert()
        self.assertEqual('Should I continue?', alert.text)
        alert.dismiss()
        alert = self.browser.get_alert()
        self.assertEqual('You say I should not', alert.text)
        alert.accept()

    def test_access_confirm_and_accept_and_dismiss_them_using_with(self):
        self.browser.visit(EXAMPLE_APP + 'alert')

        self.browser.find_by_tag('h3').first.click()
        with self.browser.get_alert() as alert:
            self.assertEqual('Should I continue?', alert.text)
            alert.accept()

        with self.browser.get_alert() as alert:
            self.assertEqual('You say I should', alert.text)
            alert.accept()

        self.browser.find_by_tag('h3').first.click()
        with self.browser.get_alert() as alert:
            self.assertEqual('Should I continue?', alert.text)
            alert.dismiss()
        with self.browser.get_alert() as alert:
            self.assertEqual('You say I should not', alert.text)
            alert.accept()

    def test_access_alerts_using_with(self):
        "should access alerts using 'with' statement"
        self.browser.visit(EXAMPLE_APP + 'alert')
        self.browser.find_by_tag('h1').first.click()
        with self.browser.get_alert() as alert:
            self.assertEqual('This is an alert example.', alert.text)
            alert.accept()
