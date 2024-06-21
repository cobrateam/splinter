# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
def test_is_element_present_by_css(browser, app_url):
    "should is element present by css verify if element is present"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_css(".async-element")


def test_is_element_present_by_css_using_a_custom_wait_time(browser, app_url):
    "should is element present by css verify if element is present using a custom wait time"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_css(".async-element2", wait_time=12)


def test_is_element_present_by_css_returns_false_if_element_is_not_present(browser, app_url):
    "should is element present by css returns False if element is not present"
    browser.visit(app_url)
    assert not browser.is_element_present_by_css(".async-elementzz")


def test_is_element_not_present_by_css(browser, app_url):
    "should is element not present by css verify if element is not present"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_css(".async-element")


def test_is_element_not_present_by_css_returns_false_if_element_is_present(browser, app_url):
    "should is element not present by css returns False if element is present"
    browser.visit(app_url)
    assert not browser.is_element_not_present_by_css("h1")


def test_is_element_not_present_by_css_using_a_custom_wait_time(browser, app_url):
    "should is element not present by css verify if element is not present using a custom wait time"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_css(".async-element", wait_time=12)


def test_is_element_present_by_xpath(browser, app_url):
    "should is element present by xpath verify if element is present"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_xpath("//h4")


def test_is_element_present_by_xpath_using_a_custom_wait_time(browser, app_url):
    "should is element present by xpath verify if element is present using a custom wait time"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_xpath("//h5", wait_time=12)


def test_is_element_present_by_xpath_returns_false_if_element_is_not_present(browser, app_url):
    "should is element present by xpath returns false if element is not present"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_xpath("//h4")


def test_is_element_not_present_by_xpath_returns_false_if_element_is_present(browser, app_url):
    """should is_element_not_present_by_xpath returns False if element is present"""
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert len(browser.find_by_xpath("//h4")) > 0
    assert not browser.is_element_not_present_by_xpath("//h4")


def test_is_element_not_present_by_xpath_using_a_custom_wait_time(browser, app_url):
    "should is element not present by xpath verify if element is not present using a custom wait time"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_xpath("//h4", wait_time=12)


def test_is_element_present_by_tag(browser, app_url):
    "should is element present by tag verify if element is present"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_tag("h4")


def test_is_element_present_by_tag_using_a_custom_wait_time(browser, app_url):
    "should is element present by tag verify if element is present using a custom wait time"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_tag("h4", wait_time=12)


def test_is_element_present_by_tag_returns_false_if_element_is_not_present(browser, app_url):
    "should is element present by tag returns false if element is not present"
    browser.visit(app_url)
    assert not browser.is_element_present_by_tag("h4")


def test_is_element_not_present_by_tag(browser, app_url):
    "should is element not present by tag verify if element is not present"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_tag("h4")


def test_is_element_not_present_by_tag_using_a_custom_wait_time(browser, app_url):
    "should is element not present by tag verify if element is not present using a custom wait time"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_tag("h4", wait_time=12)


def test_is_element_not_present_by_tag_returns_false_if_element_is_present(browser, app_url):
    """should is_element_not_present_by_tag returns False if element is present"""
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    browser.find_by_tag("h4")
    assert not browser.is_element_not_present_by_tag("h4")


def test_is_element_present_by_text(browser, app_url):
    "should is element present by text verify if element is present"
    browser.visit(app_url)
    assert browser.is_element_present_by_text("Complex")


def test_is_element_present_by_text_returns_false_if_element_is_not_present(browser, app_url):
    "should is element present by text verify if element is present"
    browser.visit(app_url)
    assert not browser.is_element_present_by_text("Not present")


def test_is_element_not_present_by_text(browser, app_url):
    "should is element not present by text verify if element is not present"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_text("Not present")


def test_is_element_not_present_by_text_returns_false_if_element_is_present(browser, app_url):
    "should is element not present by text returns False if element is present"
    browser.visit(app_url)
    assert not browser.is_element_not_present_by_text("Complex")


def test_is_element_present_by_value(browser, app_url):
    "should is element present by value verify if element is present"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_value("async-header-value")


def test_is_element_present_by_value_using_a_custom_wait_time(browser, app_url):
    "should is element present by value verify if element is present using a custom wait time"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_value("async-header-value", wait_time=12)


def test_is_element_present_by_value_returns_false_if_element_is_not_present(browser, app_url):
    "should is element present by value returns False if element is not present"
    browser.visit(app_url)
    assert not browser.is_element_present_by_value("async-header-value")


def test_is_element_not_present_by_value(browser, app_url):
    "should is element not present by value verify if element is not present"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_value("async-header-value")


def test_is_element_not_present_by_value_using_a_custom_wait_time(browser, app_url):
    "should is element not present by value verify if element is not present using a custom wait time"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_value(
        "async-header-value",
        wait_time=12,
    )


def test_is_element_not_present_by_value_returns_false_if_element_is_present(browser, app_url):
    "should is element not present by value returns False if element is present"
    browser.visit(app_url)
    assert not browser.is_element_not_present_by_value("default value")


def test_is_element_present_by_id(browser, app_url):
    "should is element present by id verify if element is present"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    result = browser.is_element_present_by_id("async-header", wait_time=20)
    assert result


def test_is_element_present_by_id_using_a_custom_wait_time(browser, app_url):
    "should is element present by id verify if element is present using a custom wait time"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_id("async-header", wait_time=12)


def test_is_element_present_by_id_returns_false_if_element_is_not_present(browser, app_url):
    "should is element present by id returns False if element is not present"
    browser.visit(app_url)
    assert not browser.is_element_present_by_id("async-header")


def test_is_element_not_present_by_id(browser, app_url):
    "should is element not present by id verify if element is not present"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_id("async-header")


def test_is_element_not_present_by_id_using_a_custom_wait_time(browser, app_url):
    "should is element not present by id verify if element is not present using a custom wait time"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_id("async-header", wait_time=12)


def test_is_element_not_present_by_id_returns_false_if_element_is_present(browser, app_url):
    """should is_element_not_present_by_id returns False if element is present"""
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    browser.find_by_id("async-header")
    assert not browser.is_element_not_present_by_id("async-header")


def test_is_element_present_by_name(browser, app_url):
    "should is element present by name verify if element is present"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_name("async-input")


def test_is_element_present_by_name_using_a_custom_wait_time(browser, app_url):
    "should is element present by name verify if element is present using a custom wait time"
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    assert browser.is_element_present_by_name("async-input", wait_time=12)


def test_is_element_present_by_name_returns_false_if_element_is_not_present(browser, app_url):
    "should is element present by name returns false if element is not present"
    browser.visit(app_url)
    assert not browser.is_element_present_by_name("async-input")


def test_is_element_not_present_by_name(browser, app_url):
    "should is element not present by name verify if element is not present"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_name("async-input")


def test_is_element_not_present_by_name_using_a_custom_wait_time(browser, app_url):
    "should is element not present by name verify if element is not present using a custom wait time"
    browser.visit(app_url)
    assert browser.is_element_not_present_by_name("async-input", wait_time=12)


def test_is_element_not_present_by_name_returns_false_if_element_is_present(browser, app_url):
    """should is_element_not_present_by_name returns False if element is present"""
    browser.visit(app_url)
    browser.find_by_css(".add-async-element").click()
    browser.find_by_name("async-input")
    assert not browser.is_element_not_present_by_name("async-input")
