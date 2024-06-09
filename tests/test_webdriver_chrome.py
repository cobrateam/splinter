# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from .base import get_browser
from .base import WebDriverTests
from .fake_webapp import EXAMPLE_APP


class TestChromeBrowser(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = get_browser("chrome", fullscreen=False)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.driver.set_window_size(1024, 768)
        self.browser.visit(EXAMPLE_APP)


class TestChromeBrowserFullscreen(WebDriverTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = get_browser("chrome", fullscreen=True)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self):
        self.browser.visit(EXAMPLE_APP)
