# Copyright 2013 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
import pytest

from .base import BaseBrowserTests
from .base import get_browser
from .fake_webapp import EXAMPLE_APP
from .lxml_drivers import LxmlDriverTests


class TestZopeTestBrowserDriver(LxmlDriverTests, BaseBrowserTests):
    @pytest.fixture(autouse=True, scope="class")
    def setup_browser(self, request):
        request.cls.browser = get_browser("zope.testbrowser", wait_time=0.1)
        request.addfinalizer(request.cls.browser.quit)

    @pytest.fixture(autouse=True)
    def visit_example_app(self, request):
        self.browser.visit(EXAMPLE_APP)

    def test_fill_form_missing_values(self):
        """Missing values should raise an error."""
        with pytest.raises(LookupError):
            self.browser.fill_form(
                {"query": "new query", "missing_form": "doesn't exist"},
            )

    def test_cookies_extra_parameters(self):
        """Cookie can be created with extra parameters."""
        comment = "Ipsum lorem"
        self.browser.cookies.add({"sha": "zam"}, comment=comment)
        cookie = self.browser._browser.cookies.getinfo("sha")
        assert "Ipsum%20lorem" == cookie["comment"]
