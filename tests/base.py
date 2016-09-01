# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from .async_finder import AsyncFinderTests
from .click_elements import ClickElementsTest
from .cookies import CookiesTest
from .element_does_not_exist import ElementDoestNotExistTest
from .fake_webapp import EXAMPLE_APP
from .find_elements import FindElementsTest
from .form_elements import FormElementsTest
from .iframes import IFrameElementsTest
from .element import ElementTest
from .is_element_present import IsElementPresentTest
from .is_element_visible import IsElementVisibleTest
from .is_text_present import IsTextPresentTest
from .mouse_interaction import MouseInteractionTest
from .status_code import StatusCodeTest
from .screenshot import ScreenshotTest
from .type import SlowlyTypeTest
from .popups import PopupWindowsTest


class BaseBrowserTests(ElementTest, FindElementsTest, FormElementsTest, ClickElementsTest,
                       CookiesTest, SlowlyTypeTest, IsTextPresentTest):

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
        html = self.browser.html
        self.assertIn('<title>Example Title</title>', html)
        self.assertIn('<h1 id="firstheader">Example Header</h1>', html)

    def test_should_reload_a_page(self):
        title = self.browser.title
        self.browser.reload()
        self.assertEqual('Example Title', title)

    def test_should_have_url(self):
        "should have access to the url"
        self.assertEqual(EXAMPLE_APP, self.browser.url)

    def test_accessing_attributes_of_links(self):
        "should allow link's attributes retrieval"
        foo = self.browser.find_link_by_text('FOO')
        self.assertEqual('http://localhost:5000/foo', foo['href'])

    def test_accessing_attributes_of_inputs(self):
        "should allow input's attributes retrieval"
        button = self.browser.find_by_css('input[name="send"]')
        self.assertEqual('send', button['name'])

    def test_accessing_attributes_of_simple_elements(self):
        "should allow simple element's attributes retrieval"
        header = self.browser.find_by_css('h1')
        self.assertEqual('firstheader', header['id'])

    def test_links_should_have_value_attribute(self):
        foo = self.browser.find_link_by_href('http://localhost:5000/foo')
        self.assertEqual('FOO', foo.value)

    def test_should_receive_browser_on_parent(self):
        "element should contains the browser on \"parent\" attribute"
        element = self.browser.find_by_id("firstheader")
        self.assertEqual(self.browser, element.parent)

    def test_redirection(self):
        """
        when visiting /redirected, browser should be redirected to /redirected-location?come=get&some=true
        browser.url should be updated
        """
        self.browser.visit('{}redirected'.format(EXAMPLE_APP))
        self.assertIn('I just been redirected to this location.', self.browser.html)
        self.assertIn('redirect-location?come=get&some=true', self.browser.url)


class WebDriverTests(BaseBrowserTests, IFrameElementsTest, ElementDoestNotExistTest, IsElementPresentTest,
                     IsElementVisibleTest, AsyncFinderTests, StatusCodeTest, MouseInteractionTest,
                     PopupWindowsTest, ScreenshotTest):

    def test_can_execute_javascript(self):
        "should be able to execute javascript"
        self.browser.execute_script("$('body').empty()")
        self.assertEqual("", self.browser.find_by_tag("body").value)

    def test_can_evaluate_script(self):
        "should evaluate script"
        self.assertEqual(8, self.browser.evaluate_script("4+4"))

    def test_can_see_the_text_for_an_element(self):
        "should provide text for an element"
        self.assertEqual(self.browser.find_by_id("simple_text").text, "my test text")

    def test_the_text_for_an_element_strips_html_tags(self):
        "should show that the text attribute strips html"
        self.assertEqual(self.browser.find_by_id("text_with_html").text, "another bit of text")

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        self.assertTrue(self.browser.find_by_id("visible").visible)

    def test_can_verify_if_a_element_is_invisible(self):
        "should provide verify if element is invisible"
        self.assertFalse(self.browser.find_by_id("invisible").visible)

    def test_default_wait_time(self):
        "should driver default wait time 2"
        self.assertEqual(2, self.browser.wait_time)

    def test_access_alerts_and_accept_them(self):
        self.browser.visit(EXAMPLE_APP + 'alert')
        self.browser.find_by_tag('h1').click()
        alert = self.browser.get_alert()
        self.assertEqual('This is an alert example.', alert.text)
        alert.accept()

    def test_access_prompts_and_be_able_to_fill_then(self):
        self.browser.visit(EXAMPLE_APP + 'alert')
        self.browser.find_by_tag('h2').click()

        alert = self.browser.get_alert()
        self.assertEqual('What is your name?', alert.text)
        alert.fill_with('Splinter')
        alert.accept()

        response = self.browser.get_alert()
        self.assertEqual('Splinter', response.text)
        response.accept()

    def test_access_confirm_and_accept_and_dismiss_them(self):
        self.browser.visit(EXAMPLE_APP + 'alert')

        self.browser.find_by_tag('h3').click()
        alert = self.browser.get_alert()

        self.assertEqual('Should I continue?', alert.text)
        alert.accept()
        alert = self.browser.get_alert()
        self.assertEqual('You say I should', alert.text)
        alert.accept()

        self.browser.find_by_tag('h3').click()
        alert = self.browser.get_alert()
        self.assertEqual('Should I continue?', alert.text)
        alert.dismiss()
        alert = self.browser.get_alert()
        self.assertEqual('You say I should not', alert.text)
        alert.accept()

    def test_access_confirm_and_accept_and_dismiss_them_using_with(self):
        self.browser.visit(EXAMPLE_APP + 'alert')

        self.browser.find_by_tag('h3').click()
        with self.browser.get_alert() as alert:
            self.assertEqual('Should I continue?', alert.text)
            alert.accept()

        with self.browser.get_alert() as alert:
            self.assertEqual('You say I should', alert.text)
            alert.accept()

        self.browser.find_by_tag('h3').click()
        with self.browser.get_alert() as alert:
            self.assertEqual('Should I continue?', alert.text)
            alert.dismiss()
        with self.browser.get_alert() as alert:
            self.assertEqual('You say I should not', alert.text)
            alert.accept()

    def test_access_alerts_using_with(self):
        "should access alerts using 'with' statement"
        self.browser.visit(EXAMPLE_APP + 'alert')
        self.browser.find_by_tag('h1').click()
        with self.browser.get_alert() as alert:
            self.assertEqual('This is an alert example.', alert.text)
            alert.accept()

    def test_can_select_a_option_via_element_text(self):
        "should provide a way to select a option via element"
        self.assertFalse(self.browser.find_option_by_value("rj").selected)
        self.browser.find_by_name("uf").select_by_text("Rio de Janeiro")
        self.assertTrue(self.browser.find_option_by_value("rj").selected)

    def test_should_be_able_to_change_user_agent(self):
        from splinter import Browser
        driver_name = self.browser.driver_name.lower()
        browser = Browser(driver_name=driver_name, user_agent="iphone")
        browser.visit(EXAMPLE_APP + "useragent")
        result = 'iphone' in browser.html
        browser.quit()
        self.assertTrue(result)
