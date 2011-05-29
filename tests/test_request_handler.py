import unittest
from fake_webapp import EXAMPLE_APP
from nose.tools import assert_equals, assert_true, assert_false, raises
from splinter.request_handler.request_handler import RequestHandler
from splinter.request_handler.status_code import HttpResponseError

class RequestHandlerTestCase(unittest.TestCase):
    def setUp(self):
        self.request = RequestHandler()
        self.request.connect(EXAMPLE_APP)

    def test_should_receive_an_url_and_get_an_success_response(self):
        assert_true(self.request.status_code.is_success())

    def test_should_start_a_request_with_localhost_and_get_localhost_as_hostname(self):
        assert_equals(self.request.host, "localhost")

    def test_should_start_a_request_with_localhost_in_port_5000_and_get_5000_as_port(self):
        assert_equals(self.request.port, 5000)

    def test_should_visit_alert_page_and_get_a_success_response(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "alert")
        assert_true(request.status_code.is_success())

    def test_should_compare_app_index_with_404_and_get_false(self):
        assert_false(self.request.status_code == 404)

    def test_should_get_an_absent_url_and_get_false_when_call_to_is_success(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
        assert_false(request.status_code.is_success())

    @raises(HttpResponseError)
    def test_should_get_an_absent_url_and_raise_an_exception(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
        request.ensures_success_response()

    def test_should_get_an_exception_and_format_it_using_the_exception_attrs(self):
        request = RequestHandler()
        request.connect(EXAMPLE_APP + "page-that-doesnt-exists")
        try:
            request.ensures_success_response()
        except HttpResponseError as e:
            exception = "I failed with code %d and reason %s" % (e.status_code, e.reason)
        assert_equals(exception, "I failed with code 404 and reason Not Found")
