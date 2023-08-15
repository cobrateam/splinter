# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from .fake_webapp import EXAMPLE_APP


supported_browsers = [
    "django",
    "flask",
    "zope.testbrowser",
]


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_css(get_new_browser, browser_name):
    "should is element present by css verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_present_by_css("h1")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_css_returns_false_if_element_is_not_present(
    get_new_browser,
    browser_name,
):
    "should is element present by css returns False if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_present_by_css(".async-elementzz")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_css(get_new_browser, browser_name):
    "should is element not present by css verify if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_not_present_by_css(".async-element")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_css_returns_false_if_element_is_present(
    get_new_browser,
    browser_name,
):
    "should is element not present by css returns False if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_not_present_by_css("h1")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_xpath(get_new_browser, browser_name):
    "should is element present by xpath verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_present_by_xpath("//h1")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_xpath_returns_false_if_element_is_not_present(
    get_new_browser,
    browser_name,
):
    "should is element present by xpath returns false if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_not_present_by_xpath("//h4")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_xpath_returns_false_if_element_is_present(
    get_new_browser,
    browser_name,
):
    "should is element not present by xpath returns false if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_not_present_by_xpath("//h1")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_tag(get_new_browser, browser_name):
    "should is element present by tag verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_present_by_tag("h1")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_tag_returns_false_if_element_is_not_present(
    get_new_browser,
    browser_name,
):
    "should is element present by tag returns false if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_present_by_tag("h4")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_tag(get_new_browser, browser_name):
    "should is element not present by tag verify if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_not_present_by_tag("h4")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_tag_returns_false_if_element_is_present(
    get_new_browser,
    browser_name,
):
    "should is element not present by tag returns false if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_not_present_by_tag("h1")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_text(get_new_browser, browser_name):
    "should is element present by text verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_present_by_text("Complex")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_text_returns_false_if_element_is_not_present(
    get_new_browser,
    browser_name,
):
    "should is element present by text verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_present_by_text("Not present")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_text(get_new_browser, browser_name):
    "should is element not present by text verify if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_not_present_by_text("Not present")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_text_returns_false_if_element_is_present(
    get_new_browser,
    browser_name,
):
    "should is element not present by text returns False if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_not_present_by_text("Complex")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_value(get_new_browser, browser_name):
    "should is element present by value verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_present_by_value("M")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_value_returns_false_if_element_is_not_present(
    get_new_browser,
    browser_name,
):
    "should is element present by value returns False if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_present_by_value("async-header-value")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_value(get_new_browser, browser_name):
    "should is element not present by value verify if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_not_present_by_value("async-header-value")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_value_returns_false_if_element_is_present(
    get_new_browser,
    browser_name,
):
    "should is element not present by value returns False if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_not_present_by_value("default value")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_id(get_new_browser, browser_name):
    "should is element present by id verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_present_by_id("firstheader")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_id_returns_false_if_element_is_not_present(
    get_new_browser,
    browser_name,
):
    "should is element present by id returns False if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_present_by_id("async-header")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_id(get_new_browser, browser_name):
    "should is element not present by id verify if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_not_present_by_id("async-header")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_id_returns_false_if_element_is_present(
    get_new_browser,
    browser_name,
):
    "should is element not present by id returns False if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_not_present_by_id("firstheader")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_name(get_new_browser, browser_name):
    "should is element present by name verify if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_present_by_name("query")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_present_by_name_returns_false_if_element_is_not_present(
    get_new_browser,
    browser_name,
):
    "should is element present by name returns false if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_present_by_name("async-input")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_name(get_new_browser, browser_name):
    "should is element not present by name verify if element is not present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert browser.is_element_not_present_by_name("async-input")


@pytest.mark.parametrize("browser_name", supported_browsers)
def test_is_element_not_present_by_name_returns_false_if_element_is_present(
    get_new_browser,
    browser_name,
):
    "should is element not present by name returns false if element is present"
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    assert not browser.is_element_not_present_by_name("query")
