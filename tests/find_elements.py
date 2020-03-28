# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from splinter.driver import ElementAPI
from splinter.element_list import ElementList


class FindElementsTest(object):
    def test_finding_by_css(self):
        value = self.browser.find_by_css("h1").value
        self.assertEqual("Example Header", value)

    def test_finding_by_xpath(self):
        value = self.browser.find_by_xpath("//h1").value
        self.assertEqual("Example Header", value)

    def test_finding_by_tag(self):
        value = self.browser.find_by_tag("h1").value
        self.assertEqual("Example Header", value)

    def test_finding_by_value(self):
        value = self.browser.find_by_value("M").value
        id = self.browser.find_by_id("gender-m")
        self.assertEqual(id.value, value)

    def test_finding_by_value_in_btn_elements(self):
        value = self.browser.find_by_value("some value").value
        btn = self.browser.find_by_id("button-value")
        self.assertEqual(btn.value, value)

    def test_finding_by_text(self):
        element = self.browser.find_by_text("Complex")
        self.assertEqual(element.value, "Complex")

    def test_finding_by_text_with_quotation_marks(self):
        element = self.browser.find_by_text("Quotation \" marks")
        self.assertEqual(element.value, "Quotation \" marks")

    def test_finding_by_id(self):
        value = self.browser.find_by_id("firstheader").value
        self.assertEqual("Example Header", value)

    def test_finding_by_name(self):
        value = self.browser.find_by_name("query").value
        self.assertEqual("default value", value)

    def test_finding_all_elements_by_css(self):
        value = self.browser.find_by_css("h1")[0].value
        self.assertEqual("Example Header", value)

    def test_finding_all_elements_by_xpath(self):
        value = self.browser.find_by_xpath("//h1")[0].value
        self.assertEqual("Example Header", value)

    def test_finding_all_elements_by_tag(self):
        value = self.browser.find_by_tag("h1")[0].value
        self.assertEqual("Example Header", value)

    def test_finding_all_elements_by_id(self):
        value = self.browser.find_by_id("firstheader").value
        self.assertEqual("Example Header", value)

    def test_finding_all_elements_by_name(self):
        value = self.browser.find_by_name("query").value
        self.assertEqual("default value", value)

    def test_finding_all_links_by_text(self):
        link = self.browser.find_link_by_text("Link for Example.com")[0]
        self.assertEqual("http://example.com/", link["href"])

    def test_finding_all_links_by_href(self):
        link = self.browser.find_link_by_href("http://example.com/")[0]
        self.assertEqual("http://example.com/", link["href"])

    def test_finding_all_links_by_partial_href(self):
        link = self.browser.find_link_by_partial_href("example.c")[0]
        self.assertEqual("http://example.com/", link["href"])

    def test_finding_all_links_by_partial_text(self):
        link = self.browser.find_link_by_partial_text("FOO")[0]
        self.assertEqual("http://localhost:5000/foo", link["href"])

    def test_finding_last_element_by_css(self):
        value = self.browser.find_by_css("h1").last.value
        self.assertEqual("Example Last Header", value)

    def test_finding_last_element_by_xpath(self):
        value = self.browser.find_by_xpath("//h1").last.value
        self.assertEqual("Example Last Header", value)

    def test_finding_last_element_by_tag(self):
        value = self.browser.find_by_tag("h1").last.value
        self.assertEqual("Example Last Header", value)

    def test_finding_last_element_by_id(self):
        value = self.browser.find_by_id("firstheader").last.value
        self.assertEqual("Example Header", value)

    def test_last_element_is_same_than_first_element_in_find_by_id(self):
        # a html page have contain one element by id
        first = self.browser.find_by_id("firstheader").value
        last = self.browser.find_by_id("firstheader").last.value
        self.assertEqual(first, last)

    def test_finding_last_element_by_name(self):
        value = self.browser.find_by_name("input1").last.value
        self.assertEqual("default last value", value)

    def test_finding_last_link_by_text(self):
        link = self.browser.find_link_by_text("Link for Example.com").last
        self.assertEqual("http://example.com/last", link["href"])

    def test_finding_last_link_by_href(self):
        link = self.browser.find_link_by_href("http://example.com/").last
        self.assertEqual("Link for last Example.com", link.text)

    def test_finding_link_by_partial_href(self):
        link = self.browser.find_link_by_partial_href("example.c").last
        self.assertEqual("Link for last Example.com", link.text)

    def test_finding_last_link_by_partial_text(self):
        link = self.browser.find_link_by_partial_text("FOO").last
        self.assertEqual("A wordier (and last) link to FOO", link.text)

    def test_finding_element_by_css_using_slice(self):
        value = self.browser.find_by_css("h1")[-1].value
        self.assertEqual("Example Last Header", value)

    def test_finding_element_by_xpath_using_slice(self):
        value = self.browser.find_by_xpath("//h1")[-1].value
        self.assertEqual("Example Last Header", value)

    def test_finding_element_by_tag_using_slice(self):
        value = self.browser.find_by_tag("h1")[-1].value
        self.assertEqual("Example Last Header", value)

    def test_finding_element_by_id_using_slice(self):
        value = self.browser.find_by_id("firstheader")[-1].value
        self.assertEqual("Example Header", value)

    def test_all_elements_is_same_than_first_element_in_find_by_id(self):
        # a html page have contain one element by id
        first = self.browser.find_by_id("firstheader").value
        some = self.browser.find_by_id("firstheader")[-1].value
        self.assertEqual(first, some)

    def test_finding_element_by_name_using_slice(self):
        value = self.browser.find_by_name("input1")[-1].value
        self.assertEqual("default last value", value)

    def test_finding_link_by_text_using_slice(self):
        link = self.browser.find_link_by_text("Link for Example.com")[-1]
        self.assertEqual("http://example.com/last", link["href"])

    def test_finding_link_by_href_using_slice(self):
        "should find link by href using slice"
        link = self.browser.find_link_by_href("http://example.com/")[-1]
        self.assertEqual("Link for last Example.com", link.text)

    def test_finding_links_by_text(self):
        "should find links by text"
        link = self.browser.find_link_by_text("Link for Example.com")
        self.assertEqual("http://example.com/", link["href"])

    def test_finding_links_by_href(self):
        "should find links by href"
        link = self.browser.find_link_by_href("http://example.com/")
        self.assertEqual("http://example.com/", link["href"])

    def test_find_by_css_in_element_context(self):
        "should find elements by css in element context and should return splinter driver element"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_css("h2")
        self.assertEqual(decendent.text.strip(), "inside")
        self.assertIsInstance(decendent, ElementList)
        self.assertIsInstance(decendent[0], ElementAPI)

    def test_find_by_xpath_in_element_context(self):
        "should find elements by xpath in element context"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_xpath("//h2")
        self.assertEqual(decendent.text.strip(), "inside")
        self.assertIsInstance(decendent, ElementList)
        self.assertIsInstance(decendent.first, ElementAPI)

    def test_find_by_name_in_element_context(self):
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_name("crazy-upload")
        self.assertEqual(len(decendent), 1)
        self.assertIsInstance(decendent, ElementList)
        self.assertIsInstance(decendent.first, ElementAPI)

    def test_find_by_tag_in_element_context(self):
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_tag("input")
        self.assertEqual(len(decendent), 1)
        self.assertIsInstance(decendent, ElementList)
        self.assertIsInstance(decendent.first, ElementAPI)

    def test_find_by_id_in_element_context(self):
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_id("visible")
        self.assertEqual(len(decendent), 1)
        self.assertIsInstance(decendent, ElementList)
        self.assertIsInstance(decendent.first, ElementAPI)

    def test_find_by_value_in_element_context(self):
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_value("crazy diamond")
        self.assertEqual(len(decendent), 1)
        self.assertIsInstance(decendent, ElementList)
        self.assertIsInstance(decendent.first, ElementAPI)

    def test_finding_by_text_in_element_context(self):
        inside = self.browser.find_by_id("inside")
        element = inside.find_by_text("Complex")

        self.assertEqual(len(element), 1)
        self.assertEqual(element["class"], "inside")
        self.assertEqual(element.value, "Complex")
