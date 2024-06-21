# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from tests.fake_webapp import app


@pytest.fixture()
def browser_kwargs():
    return {"app": app, "wait_time": 0.1}


def test_serialize_select_mutiple(browser, app_url):
    """should serialize a select with multiple values into a list"""
    browser.visit(app_url)
    browser.select("pets", ["cat", "dog"])
    form = browser.find_by_name("send")._get_parent_form()
    data = browser.serialize(form)
    assert data["pets"] == ["cat", "dog"]


def test_redirection_on_post(browser, app_url):
    """
    when submitting a form that POSTs to /redirected,
    browser should be redirected to GET /redirected-location?come=get&some=true
    """
    browser.visit(app_url)
    browser.find_by_name("redirect").click()
    assert "I just been redirected to this location" in browser.html
    assert "redirect-location?come=get&some=true" in browser.url
