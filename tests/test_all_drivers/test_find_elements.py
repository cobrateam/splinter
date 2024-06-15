# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from splinter.driver import ElementAPI
from splinter.element_list import ElementList


def test_finding_by_css(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_css("h1").value
    assert "Example Header" == value


def test_finding_by_xpath(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_xpath("//h1").value
    assert "Example Header" == value


def test_finding_by_tag(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_tag("h1").value
    assert "Example Header" == value


def test_finding_by_value(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_value("M").value
    element = browser.find_by_id("gender-m")
    assert element.value == value


def test_finding_by_value_in_btn_elements(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_value("some value").value
    btn = browser.find_by_id("button-value")
    assert btn.value == value


def test_finding_by_text(browser, app_url):
    browser.visit(app_url)
    element = browser.find_by_text("Complex")
    assert element.value == "Complex"


def test_finding_by_text_with_quotation_marks(browser, app_url):
    browser.visit(app_url)
    element = browser.find_by_text('Quotation " marks')
    assert element.value == 'Quotation " marks'


def test_finding_by_id(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_id("firstheader").value
    assert "Example Header" == value


def test_finding_by_name(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_name("query").value
    assert "default value" == value


def test_finding_all_elements_by_css(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_css("h1")[0].value
    assert "Example Header" == value


def test_finding_all_elements_by_xpath(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_xpath("//h1")[0].value
    assert "Example Header" == value


def test_finding_all_elements_by_tag(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_tag("h1")[0].value
    assert "Example Header" == value


def test_finding_all_elements_by_id(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_id("firstheader").value
    assert "Example Header" == value


def test_finding_all_elements_by_name(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_name("query").value
    assert "default value" == value


def test_finding_all_links_by_text(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_text("Link for Example.com")[0]
    assert "http://example.com/" == link["href"]


def test_finding_all_links_by_href(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_href("http://example.com/")[0]
    assert "http://example.com/" == link["href"]


def test_finding_all_links_by_partial_href(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_partial_href("example.c")[0]
    assert "http://example.com/" == link["href"]


def test_finding_all_links_by_partial_text(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_partial_text("FOO")[0]
    assert "http://localhost:5000/foo" == link["href"]


def test_find_links_by_partial_text_nested_elements(browser, app_url):
    """
    When text is split in multiple child elements of a parent link element
    Then the parent link element is found
    """
    browser.visit(app_url)

    expected = "http://localhost:5000/nested"

    link = browser.links.find_by_partial_text("Nested text")[0]
    assert expected == link["href"]

    link = browser.links.find_by_partial_text("in a link")[0]
    assert expected == link["href"]

    link = browser.links.find_by_partial_text("Nested text in")[0]
    assert expected == link["href"]

    link = browser.links.find_by_partial_text("text in a link")[0]
    assert expected == link["href"]

    link = browser.links.find_by_partial_text("Nested text in a link")[0]
    assert expected == link["href"]


def test_finding_last_element_by_css(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_css("h1").last.value
    assert "Example Last Header" == value


def test_finding_last_element_by_xpath(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_xpath("//h1").last.value
    assert "Example Last Header" == value


def test_finding_last_element_by_tag(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_tag("h1").last.value
    assert "Example Last Header" == value


def test_finding_last_element_by_id(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_id("firstheader").last.value
    assert "Example Header" == value


def test_last_element_is_same_than_first_element_in_find_by_id(browser, app_url):
    browser.visit(app_url)
    # a html page have contain one element by id
    first = browser.find_by_id("firstheader").value
    last = browser.find_by_id("firstheader").last.value
    assert first == last


def test_finding_last_element_by_name(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_name("input1").last.value
    assert "default last value" == value


def test_finding_last_link_by_text(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_text("Link for Example.com").last
    assert "http://example.com/last" == link["href"]


def test_finding_last_link_by_href(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_href("http://example.com/").last
    assert "Link for last Example.com" == link.text


def test_finding_link_by_partial_href(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_partial_href("example.c").last
    assert "Link for last Example.com" == link.text


def test_finding_last_link_by_partial_text(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_partial_text("FOO").last
    assert "A wordier (and last) link to FOO" == link.text


def test_finding_element_by_css_using_slice(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_css("h1")[-1].value
    assert "Example Last Header" == value


def test_finding_element_by_xpath_using_slice(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_xpath("//h1")[-1].value
    assert "Example Last Header" == value


def test_finding_element_by_tag_using_slice(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_tag("h1")[-1].value
    assert "Example Last Header" == value


def test_finding_element_by_id_using_slice(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_id("firstheader")[-1].value
    assert "Example Header" == value


def test_all_elements_is_same_than_first_element_in_find_by_id(browser, app_url):
    browser.visit(app_url)
    # a html page have contain one element by id
    first = browser.find_by_id("firstheader").value
    some = browser.find_by_id("firstheader")[-1].value
    assert first == some


def test_finding_element_by_name_using_slice(browser, app_url):
    browser.visit(app_url)
    value = browser.find_by_name("input1")[-1].value
    assert "default last value" == value


def test_finding_link_by_text_using_slice(browser, app_url):
    browser.visit(app_url)
    link = browser.links.find_by_text("Link for Example.com")[-1]
    assert "http://example.com/last" == link["href"]


def test_finding_link_by_href_using_slice(browser, app_url):
    "should find link by href using slice"
    browser.visit(app_url)
    link = browser.links.find_by_href("http://example.com/")[-1]
    assert "Link for last Example.com" == link.text


def test_finding_links_by_text(browser, app_url):
    "should find links by text"
    browser.visit(app_url)
    link = browser.links.find_by_text("Link for Example.com")
    assert "http://example.com/" == link["href"]


def test_finding_links_by_href(browser, app_url):
    "should find links by href"
    browser.visit(app_url)
    link = browser.links.find_by_href("http://example.com/")
    assert "http://example.com/" == link["href"]


def test_find_by_css_in_element_context(browser, app_url):
    "should find elements by css in element context and should return splinter driver element"
    browser.visit(app_url)
    elements = browser.find_by_css("#inside")
    decendent = elements[0].find_by_css("h2")
    assert decendent.text.strip() == "inside"
    assert isinstance(decendent, ElementList)
    assert isinstance(decendent[0], ElementAPI)


def test_find_by_xpath_in_element_context(browser, app_url):
    "should find elements by xpath in element context"
    browser.visit(app_url)
    elements = browser.find_by_css("#inside")
    decendent = elements[0].find_by_xpath("//h2")
    assert decendent.text.strip() == "inside"
    assert isinstance(decendent, ElementList)
    assert isinstance(decendent.first, ElementAPI)


def test_find_by_name_in_element_context(browser, app_url):
    browser.visit(app_url)
    elements = browser.find_by_css("#inside")
    decendent = elements[0].find_by_name("crazy-upload")
    assert len(decendent) == 1
    assert isinstance(decendent, ElementList)
    assert isinstance(decendent.first, ElementAPI)


def test_find_by_tag_in_element_context(browser, app_url):
    browser.visit(app_url)
    elements = browser.find_by_css("#inside")
    decendent = elements[0].find_by_tag("input")
    assert len(decendent) == 1
    assert isinstance(decendent, ElementList)
    assert isinstance(decendent.first, ElementAPI)


def test_find_by_id_in_element_context(browser, app_url):
    browser.visit(app_url)
    elements = browser.find_by_css("#inside")
    decendent = elements[0].find_by_id("visible")
    assert len(decendent) == 1
    assert isinstance(decendent, ElementList)
    assert isinstance(decendent.first, ElementAPI)


def test_find_by_value_in_element_context(browser, app_url):
    browser.visit(app_url)
    elements = browser.find_by_css("#inside")
    decendent = elements[0].find_by_value("crazy diamond")
    assert len(decendent) == 1
    assert isinstance(decendent, ElementList)
    assert isinstance(decendent.first, ElementAPI)


def test_finding_by_text_in_element_context(browser, app_url):
    browser.visit(app_url)
    inside = browser.find_by_id("inside")
    element = inside.find_by_text("Complex")

    assert len(element) == 1
    assert element["class"] == "inside"
    assert element.value == "Complex"
