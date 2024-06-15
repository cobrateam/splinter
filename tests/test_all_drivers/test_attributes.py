# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


def test_with_statement(browser):
    """When I use a browser as a context manager
    Then the context manager's target is the browser object
    """
    with browser as b:
        assert b is not None


def test_should_have_html(browser, app_url):
    browser.visit(app_url)
    html = browser.html
    assert "<title>Example Title</title>" in html
    assert '<h1 id="firstheader">Example Header</h1>' in html


def test_should_have_url(browser, app_url):
    "should have access to the url"
    browser.visit(app_url)
    assert app_url == browser.url


def test_accessing_attributes_of_links(browser, app_url):
    "should allow link's attributes retrieval"
    browser.visit(app_url)
    foo = browser.links.find_by_text("FOO")
    assert "http://localhost:5000/foo" == foo["href"]


def test_accessing_attributes_of_inputs(browser, app_url):
    "should allow input's attributes retrieval"
    browser.visit(app_url)
    button = browser.find_by_css('input[name="send"]')
    assert "send" == button["name"]


def test_accessing_attributes_of_simple_elements(browser, app_url):
    "should allow simple element's attributes retrieval"
    browser.visit(app_url)
    header = browser.find_by_css("h1")
    assert "firstheader" == header["id"]


def test_links_should_have_value_attribute(browser, app_url):
    browser.visit(app_url)
    foo = browser.links.find_by_href("http://localhost:5000/foo")
    assert "FOO" == foo.value


def test_should_receive_browser_on_parent(browser, app_url):
    'element should contains the browser on "parent" attribute'
    browser.visit(app_url)
    element = browser.find_by_id("firstheader")
    assert browser == element.parent
