# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
def test_can_work_on_iframes_by_name(browser, app_url):
    """can work on iframes and switch back to the page"""
    browser.visit(app_url)

    with browser.get_iframe("iframemodal-name") as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value


def test_can_work_on_iframes_by_id(browser, app_url):
    """can work on iframes and switch back to the page"""
    browser.visit(app_url)

    with browser.get_iframe("iframemodal") as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value


def test_can_work_on_iframes_by_webelement(browser, app_url):
    """can work on iframes and switch back to the page"""
    browser.visit(app_url)

    elem = browser.find_by_id("iframemodal").first

    with browser.get_iframe(elem) as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value


def test_can_work_on_iframes_by_index(browser, app_url):
    """can work on iframes and switch back to the page"""
    browser.visit(app_url)

    with browser.get_iframe(0) as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value
