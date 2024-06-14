# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from tests.base import get_browser
from tests.base import WebDriverTests
from tests.fake_webapp import EXAMPLE_APP

from splinter.config import Config


class TestFirefoxBrowser(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        config = Config(fullscreen=False, headless=True)
        request.cls.browser = get_browser("firefox", config=config)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)


class TestFirefoxBrowserFullScreen(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        config = Config(fullscreen=True, headless=True)
        request.cls.browser = get_browser("firefox", config=config)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)
