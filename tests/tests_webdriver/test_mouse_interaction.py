# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import time

import pytest


@pytest.mark.flaky
def test_mouse_over(browser, app_url):
    "Should be able to perform a mouse over on an element"
    browser.visit(app_url)

    element = browser.find_by_css(".add-element-mouseover")
    element.mouse_over()

    time.sleep(5)
    assert browser.is_element_present_by_id("what-is-your-name", wait_time=10)

    element = browser.find_by_css(".add-element-mouseover")
    element.mouse_out()

    assert browser.is_element_not_present_by_id("what-is-your-name", wait_time=10)


@pytest.mark.flaky
def test_mouse_out(browser, app_url):
    "Should be able to perform a mouse out on an element"
    browser.visit(app_url)

    element = browser.find_by_css(".add-element-mouseover")
    element.mouse_over()
    element.mouse_out()

    assert browser.is_element_not_present_by_id("what-is-your-name", wait_time=10)


@pytest.mark.flaky
def test_mouse_out_top_left(browser, app_url):
    """Should be able to perform a mouse out on an element,
    even if the element is at the top left corner of the screen.
    """
    browser.visit(app_url + "/mouse")

    element = browser.find_by_css(".add-element-mouseover")
    element.mouse_over()
    element.mouse_out()

    assert browser.is_element_not_present_by_id("what-is-your-name", wait_time=10)


@pytest.mark.flaky
def test_double_click(browser, app_url):
    """Test: WebDriverElement.double_click()

    When an element has an action activated by a double click
    Then using the double_click() method will trigger it
    """
    browser.visit(app_url)

    button = browser.find_by_css(".db-button", wait_time=10)
    button.double_click()

    assert browser.find_by_css(
        ".should-be-visible-after-double-click",
        wait_time=10,
    ).is_visible(
        wait_time=10,
    )
    assert browser.is_element_not_present_by_id("what-is-your-name", wait_time=20)


@pytest.mark.flaky
def test_right_click(browser, app_url):
    "should be able to perform a right click on an element"
    browser.visit(app_url)

    element = browser.find_by_css(".right-clicable")
    element.right_click()

    time.sleep(5)
    result_1 = browser.find_by_text("right clicked", wait_time=20).text
    result_2 = browser.find_by_css(".right-clicable", wait_time=20).text

    assert result_1 == result_2 == "right clicked"


@pytest.mark.flaky
def test_drag_and_drop(browser, app_url):
    """
    should be able to perform a drag an element and drop in another element
    """
    browser.visit(app_url)

    droppable = browser.find_by_css(".droppable")
    draggable = browser.find_by_css(".draggable")
    draggable.drag_and_drop(droppable)

    time.sleep(5)
    assert "yes" == browser.find_by_css(".dragged").text
