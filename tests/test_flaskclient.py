# Copyright 2014 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import time

import pytest

from .base import BaseBrowserTests
from .base import get_browser
from .fake_webapp import app
from .fake_webapp import EXAMPLE_APP
from .lxml_drivers import LxmlDriverTests


class TestFlaskClientDriver(LxmlDriverTests, BaseBrowserTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = get_browser("flask", app=app, wait_time=0.1)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)

    def test_serialize_select_mutiple(self):
        """should serialize a select with multiple values into a list"""
        self.browser.select("pets", ["cat", "dog"])
        form = self.browser.find_by_name("send")._get_parent_form()
        data = self.browser.serialize(form)
        assert data["pets"] == ["cat", "dog"]

    def test_redirection_on_post(self):
        """
        when submitting a form that POSTs to /redirected,
        browser should be redirected to GET /redirected-location?come=get&some=true
        """
        self.browser.find_by_name("redirect").click()
        assert "I just been redirected to this location" in self.browser.html
        assert "redirect-location?come=get&some=true" in self.browser.url

    def test_cookies_extra_parameters(self):
        """Cookie can be created with extra parameters."""
        timestamp = int(time.time() + 120)
        self.browser.cookies.add({"sha": "zam"}, expires=timestamp)
        cookie = {c.key: c for c in self.browser._browser._cookies.values()}["sha"]
        assert timestamp == int(cookie.expires.timestamp())


class TestFlaskClientDriverWithCustomHeaders:
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        custom_headers = {
            "X-Splinter-Customheaders-1": "Hello",
            "X-Splinter-Customheaders-2": "Bye",
        }
        request.cls.browser = get_browser("flask", app=app, wait_time=0.1, custom_headers=custom_headers)
        request.addfinalizer(request.cls.browser.quit)

    def test_create_a_flask_client_with_custom_headers(self):
        self.browser.visit(EXAMPLE_APP + "headers")
        assert self.browser.is_text_present("X-Splinter-Customheaders-1: Hello")
        assert self.browser.is_text_present("X-Splinter-Customheaders-2: Bye")
