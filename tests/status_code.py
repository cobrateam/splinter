# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.
from .fake_webapp import EXAMPLE_APP


class StatusCodeTest:
    def test_should_visit_index_of_example_app_and_get_200_status_code(self):
        self.browser.visit(EXAMPLE_APP)
        assert 200 == self.browser.status_code
        assert "200 - OK" == str(self.browser.status_code)

    def test_should_visit_error_of_example_app_and_not_get_200_status_code(self):
        self.browser.visit(EXAMPLE_APP + "error.html")
        assert 200 != self.browser.status_code
        assert "404 - Not Found" == str(self.browser.status_code)
