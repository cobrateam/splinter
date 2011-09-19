# -*- coding: utf-8 -*-

from __future__ import with_statement

import warnings
from nose.tools import assert_equals

from splinter.driver import ElementAPI
from splinter.element_list import ElementList


class FindElementsTest(object):

    def test_finding_by_css(self):
        "should finds by css"
        value = self.browser.find_by_css('h1').first.value
        assert_equals('Example Header', value)

    def test_finding_by_xpath(self):
        "should find elements by xpath"
        value = self.browser.find_by_xpath('//h1').first.value
        assert_equals('Example Header', value)

    def test_finding_by_tag(self):
        "should find elements by tag"
        value = self.browser.find_by_tag('h1').first.value
        assert_equals('Example Header', value)

    def test_finding_by_value(self):
        "should find elements by value"
        value = self.browser.find_by_value('M').first.value
        id = self.browser.find_by_id('gender-m')
        assert_equals(id.first.value ,value)

    def test_finding_by_id(self):
        "should find elements by id"
        value = self.browser.find_by_id("firstheader").first.value
        assert_equals('Example Header', value)

    def test_finding_by_name(self):
        "should find elements by name"
        value = self.browser.find_by_name('query').first.value
        assert_equals('default value', value)

    def test_finding_all_elements_by_css(self):
        "should find elements by css"
        value = self.browser.find_by_css('h1')[0].value
        assert_equals('Example Header', value)

    def test_finding_all_elements_by_xpath(self):
        "should find elements by xpath"
        value = self.browser.find_by_xpath('//h1')[0].value
        assert_equals('Example Header', value)

    def test_finding_all_elements_by_tag(self):
        "should find elements by tag"
        value = self.browser.find_by_tag('h1')[0].value
        assert_equals('Example Header', value)

    def test_finding_all_elements_by_id(self):
        "should find elements by id"
        value = self.browser.find_by_id("firstheader")[0].value
        assert_equals('Example Header', value)

    def test_finding_all_elements_by_name(self):
        "should find elements by name"
        value = self.browser.find_by_name('query')[0].value
        assert_equals('default value', value)

    def test_finding_all_links_by_text(self):
        "should find links by text"
        link = self.browser.find_link_by_text('Link for Example.com')[0]
        assert_equals('http://example.com/', link['href'])

    def test_finding_all_links_by_href(self):
        "should find links by href"
        link = self.browser.find_link_by_href('http://example.com/')[0]
        assert_equals('http://example.com/', link['href'])

    def test_finding_all_links_by_partial_href(self):
        "should find links by partial href"
        link = self.browser.find_link_by_partial_href('example.c')[0]
        assert_equals('http://example.com/', link['href'])

    def test_finding_all_links_by_partial_text(self):
        "should find links by partial text"
        link = self.browser.find_link_by_partial_text('FOO')[0]
        assert_equals('http://localhost:5000/foo', link['href'])

    def test_finding_last_element_by_css(self):
        "should find last element by css"
        value = self.browser.find_by_css('h1').last.value
        assert_equals('Example Last Header', value)

    def test_finding_last_element_by_xpath(self):
        "should find last element by xpath"
        value = self.browser.find_by_xpath('//h1').last.value
        assert_equals('Example Last Header', value)

    def test_finding_last_element_by_tag(self):
        "should find last element by tag"
        value = self.browser.find_by_tag('h1').last.value
        assert_equals('Example Last Header', value)

    def test_finding_last_element_by_id(self):
        "should find last element by id"
        value = self.browser.find_by_id("firstheader").last.value
        assert_equals('Example Header', value)

    def test_last_element_is_same_than_first_element_in_find_by_id(self):
        "should first element is same than last element in find by id"
        #a html page have contain one element by id
        first = self.browser.find_by_id("firstheader").first.value
        last = self.browser.find_by_id("firstheader").last.value
        assert_equals(first, last)

    def test_finding_last_element_by_name(self):
        "should find last element by name"
        value = self.browser.find_by_name('query').last.value
        assert_equals('default last value', value)

    def test_finding_last_link_by_text(self):
        "should find last link by text"
        link = self.browser.find_link_by_text('Link for Example.com').last
        assert_equals('http://example.com/last', link['href'])

    def test_finding_last_link_by_href(self):
        "should find last link by href"
        link = self.browser.find_link_by_href('http://example.com/').last
        assert_equals('Link for last Example.com', link.text)

    def test_finding_link_by_partial_href(self):
        "should find links by partial href"
        link = self.browser.find_link_by_partial_href('example.c').last
        assert_equals('Link for last Example.com', link.text)

    def test_finding_last_link_by_partial_text(self):
        "should find last link by partial text"
        link = self.browser.find_link_by_partial_text('FOO').last
        assert_equals('A wordier (and last) link to FOO', link.text)

    def test_finding_element_by_css_using_slice(self):
        "should find element by css using slice"
        value = self.browser.find_by_css('h1')[-1].value
        assert_equals('Example Last Header', value)

    def test_finding_element_by_xpath_using_slice(self):
        "should find element by xpath using slice"
        value = self.browser.find_by_xpath('//h1')[-1].value
        assert_equals('Example Last Header', value)

    def test_finding_element_by_tag_using_slice(self):
        "should find element by tag using slice"
        value = self.browser.find_by_tag('h1')[-1].value
        assert_equals('Example Last Header', value)

    def test_finding_element_by_id_using_slice(self):
        "should find element by id using slice"
        value = self.browser.find_by_id("firstheader")[-1].value
        assert_equals('Example Header', value)

    def test_all_elements_is_same_than_first_element_in_find_by_id(self):
        "should all elements is same than first element in find by id"
        #a html page have contain one element by id
        first = self.browser.find_by_id("firstheader").first.value
        some = self.browser.find_by_id("firstheader")[-1].value
        assert_equals(first, some)

    def test_finding_element_by_name_using_slice(self):
        "should find element by name using slice"
        value = self.browser.find_by_name('query')[-1].value
        assert_equals('default last value', value)

    def test_finding_link_by_text_using_slice(self):
        "should find link by text using slice"
        link = self.browser.find_link_by_text('Link for Example.com')[-1]
        assert_equals('http://example.com/last', link['href'])

    def test_finding_link_by_href_using_slice(self):
        "should find link by href using slice"
        link = self.browser.find_link_by_href('http://example.com/')[-1]
        assert_equals('Link for last Example.com', link.text)

    def test_finding_links_by_text(self):
        "should find links by text"
        link = self.browser.find_link_by_text('Link for Example.com').first
        assert_equals('http://example.com/', link['href'])

    def test_finding_links_by_href(self):
        "should find links by href"
        link = self.browser.find_link_by_href('http://example.com/').first
        assert_equals('http://example.com/', link['href'])

    def test_find_by_css_in_element_context(self):
        "should find elements by css in element context and should return splinter driver element"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_css('h2')
        assert_equals(decendent.first.text.strip(), 'inside')
        assert isinstance(decendent, ElementList)
        assert isinstance(decendent[0], ElementAPI)

    def test_find_by_xpath_in_element_context(self):
        "should find elements by xpath in element context"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_xpath("//h2")
        assert_equals(decendent.first.text.strip(), 'inside')
        assert isinstance(decendent, ElementList)
        assert isinstance(decendent[0], ElementAPI)

    def test_find_by_name_in_element_context(self):
        "should find elements by name in element context"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_name("upload")
        assert_equals(len(decendent), 1)
        assert isinstance(decendent, ElementList)
        assert isinstance(decendent[0], ElementAPI)

    def test_find_by_tag_in_element_context(self):
        "should find elements by tag in element context"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_tag("input")
        assert_equals(len(decendent), 1)
        assert isinstance(decendent, ElementList)
        assert isinstance(decendent[0], ElementAPI)

    def test_find_by_id_in_element_context(self):
        "should find elements by id in element context"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_id("visible")
        assert_equals(len(decendent), 1)
        assert isinstance(decendent, ElementList)
        assert isinstance(decendent[0], ElementAPI)

    def test_find_by_value_in_element_context(self):
        "should find elements by value in element context"
        elements = self.browser.find_by_css("#inside")
        decendent = elements[0].find_by_value("crazy diamond")
        assert_equals(len(decendent), 1)
        assert isinstance(decendent, ElementList)
        assert isinstance(decendent[0], ElementAPI)
