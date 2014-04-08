# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from .fake_webapp import EXAMPLE_APP
from splinter.request_handler.status_code import HttpResponseError


class StatusCodeTest(object):

    def test_should_visit_an_absent_page_and_get_an_404_error(self):
        with self.assertRaises(HttpResponseError):
            self.browser.visit(EXAMPLE_APP + "this_page_does_not_exists")

    def test_should_visit_index_of_example_app_and_get_200_status_code(self):
        self.browser.visit(EXAMPLE_APP)
        self.assertEqual(200, self.browser.status_code)

    def test_should_be_able_to_print_status_code_with_reason(self):
        self.browser.visit(EXAMPLE_APP)
        self.assertEqual('200 - OK', str(self.browser.status_code))
