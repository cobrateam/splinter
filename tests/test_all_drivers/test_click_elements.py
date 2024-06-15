# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os

import pytest


skip_if_safari = pytest.mark.skipif(
    os.getenv("SAFARI"),
    reason="Test not compatible with safari",
)


@skip_if_safari
def test_click_links(browser, app_url):
    browser.visit(app_url)
    browser.links.find_by_text("FOO").click()
    assert "BAR!" in browser.html


@skip_if_safari
def test_click_element_by_css_selector(browser, app_url):
    browser.visit(app_url)
    browser.find_by_css('a[href="http://localhost:5000/foo"]').click()
    assert "BAR!" in browser.html


@skip_if_safari
def test_click_input_by_css_selector(browser, app_url):
    browser.visit(app_url)
    browser.find_by_css('input[name="send"]').click()
    assert "My name is: Master Splinter" in browser.html
