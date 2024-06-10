# Copyright 2015 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import os
import sys
import time

import django
import pytest

from .base import BaseBrowserTests
from .base import get_browser
from .fake_webapp import EXAMPLE_APP
from .lxml_drivers import LxmlDriverTests


sys.path.append("tests/fake_django")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"


django.setup()


class TestDjangoClientDriver(LxmlDriverTests, BaseBrowserTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = get_browser("django")
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self):
        self.browser.visit(EXAMPLE_APP)

    def test_cookies_extra_parameters(self):
        """Cookie can be created with extra parameters."""
        timestamp = int(time.time() + 120)
        self.browser.cookies.add({"sha": "zam"}, expires=timestamp)
        cookie = self.browser._browser.cookies["sha"]
        assert timestamp == cookie["expires"]


class TestDjangoClientDriverWithCustomHeaders:
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        custom_headers = {
            "X-Splinter-Customheaders-1": "Hello",
            "X-Splinter-Customheaders-2": "Bye",
        }
        request.cls.browser = get_browser("django", custom_headers=custom_headers)
        request.addfinalizer(request.cls.browser.quit)

    def test_create_a_browser_with_custom_headers(self):
        self.browser.visit(EXAMPLE_APP + "headers")
        assert self.browser.is_text_present("X-Splinter-Customheaders-1: Hello")

        assert self.browser.is_text_present("X-Splinter-Customheaders-2: Bye")
