# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from .base import supported_browsers
from .get_browser import get_browser
from .fake_webapp import EXAMPLE_APP

import pytest


@pytest.fixture
def get_new_browser(request):
    def new_browser(browser_name):
        browser = get_browser(browser_name)
        request.addfinalizer(browser.quit)
        return browser
    return new_browser


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_can_work_on_iframes_by_name(get_new_browser, browser_name):
    """can work on iframes and switch back to the page"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    with browser.get_iframe("iframemodal-name") as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_can_work_on_iframes_by_id(get_new_browser, browser_name):
    """can work on iframes and switch back to the page"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    with browser.get_iframe("iframemodal") as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_can_work_on_iframes_by_webelement(get_new_browser, browser_name):
    """can work on iframes and switch back to the page"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    elem = browser.find_by_id('iframemodal').first

    with browser.get_iframe(elem) as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value


@pytest.mark.parametrize('browser_name', supported_browsers)
def test_can_work_on_iframes_by_index(get_new_browser, browser_name):
    """can work on iframes and switch back to the page"""
    browser = get_new_browser(browser_name)
    browser.visit(EXAMPLE_APP)

    with browser.get_iframe(0) as frame:
        value = frame.find_by_tag("h1").value
        assert "IFrame Example Header" == value

    value = browser.find_by_tag("h1").value
    assert "Example Header" == value
