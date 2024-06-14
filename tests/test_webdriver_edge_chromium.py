# Copyright 2021 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from .base import get_browser
from .base import WebDriverTests
from .fake_webapp import EXAMPLE_APP

from splinter.config import Config


class TestEdgeChromiumBrowser(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        config = Config(fullscreen=False, headless=True)
        request.cls.browser = get_browser("edge", config=config)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.driver.set_window_size(1024, 768)
        self.browser.visit(EXAMPLE_APP)


class TestEdgeChromiumBrowserFullscreen(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        config = Config(fullscreen=True, headless=True)
        request.cls.browser = get_browser("edge", config=config)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self):
        self.browser.visit(EXAMPLE_APP)
