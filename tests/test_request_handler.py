# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os

try:
    import unittest2 as unittest
except ImportError:
    import unittest

from fake_webapp import EXAMPLE_APP
from splinter.request_handler.request_handler import RequestHandler
from splinter.request_handler.status_code import HttpResponseError
from tests import TESTS_ROOT


class RequestHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.request = RequestHandler()
        self.request.connect(EXAMPLE_APP)

    def test_should_receive_an_url_and_get_a_success_response(self):
        self.assertTrue(self.request.status_code.is_success())

    def test_should_start_a_request_with_localhost_and_get_localhost_as_hostname(self):
        self.assertEqual("localhost", self.request.host)

    def test_should_start_a_request_with_localhost_in_port_5000_and_get_5000_as_port(self):
        self.assertEqual(5000, self.request.port)

    def test_should_visit_alert_page_and_get_a_success_response(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "alert")
        self.assertTrue(request.status_code.is_success())

    def test_should_compare_app_index_with_404_and_get_false(self):
        self.assertFalse(self.request.status_code == 404)

    def test_should_get_an_absent_url_and_get_false_when_call_to_is_success(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
        self.assertFalse(request.status_code.is_success())

    def test_should_get_an_absent_url_and_raise_an_exception(self):
        with self.assertRaises(HttpResponseError):
            request = RequestHandler()
            request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
            request.ensure_success_response()

    def test_should_get_an_exception_and_format_it_using_the_exception_attrs(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
        try:
            request.ensure_success_response()
        except HttpResponseError as e:
            exception = e.msg
        self.assertEqual("404 - Not Found", exception)

    def test_should_be_able_to_represent_exception_as_string(self):
        "HttpResponseError exception should be representable as string"
        error = HttpResponseError(404, "Not Found")
        self.assertEqual("404 - Not Found", str(error))

    def test_should_not_connect_to_non_http_protocols(self):
        mockfile_path = "file://%s" % os.path.join(TESTS_ROOT, "mockfile.txt")
        request = RequestHandler()
        request.connect(mockfile_path)
        self.assertTrue(request.status_code.is_success())

    def test_should_connect_to_pages_with_query_string(self):
        request = RequestHandler()
        url = EXAMPLE_APP + "query?model"
        request.connect(url)
        self.assertTrue(request.status_code.is_success())
