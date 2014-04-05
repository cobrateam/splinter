# -*- coding: utf-8 -*-

# Copyright 2012 splinter authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import unittest

from ssl import SSLError

from .fake_webapp import EXAMPLE_APP
from splinter.request_handler.request_handler import RequestHandler
from splinter.request_handler.status_code import HttpResponseError
from tests import TESTS_ROOT


class RequestHandlerTestCase(unittest.TestCase):

    def setUp(self):
        self.request = RequestHandler()
        self.request.connect(EXAMPLE_APP)

    def test_should_receive_an_url_and_get_a_success_response(self):
        self.assertTrue(self.request.status_code.is_success())

    def test_should_start_a_request_with_localhost(self):
        self.assertEqual("127.0.0.1", self.request.host)

    def test_should_start_a_request_with_port_5000(self):
        self.assertEqual(5000, self.request.port)

    def test_should_visit_alert_page_and_get_a_success_response(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "alert")
        self.assertTrue(request.status_code.is_success())

    def test_should_compare_app_index_with_404_and_get_false(self):
        self.assertFalse(self.request.status_code == 404)

    def test_is_success_should_be_false_when_url_does_not_exists(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
        self.assertFalse(request.status_code.is_success())

    def test_should_get_an_absent_url_and_raise_an_exception(self):
        with self.assertRaises(HttpResponseError):
            request = RequestHandler()
            request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
            request.ensure_success_response()

    def test_should_get_an_exception_and_format_it(self):
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

    def test_should_connect_to_https_protocols(self):
        # We do not run an HTTPS server, but we know we handle https
        # if we get an SSLError accessing a non-HTTPS site.
        with self.assertRaises(SSLError):
            request = RequestHandler()
            url = EXAMPLE_APP.replace('http', 'https')
            request.connect(url)
            self.assertEqual(request.scheme, 'https')

    def test_should_set_user_agent(self):
        request = RequestHandler()
        url = EXAMPLE_APP + 'useragent'
        request.connect(url)
        self.assertEqual('python/splinter', request.response.read())

    def test_should_be_able_to_connect_with_basic_auth(self):
        request = RequestHandler()
        url = 'http://admin:secret@localhost:5000/authenticate'
        request.connect(url)
        self.assertEqual('Success!', request.response.read())
