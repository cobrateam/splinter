from fake_webapp import EXAMPLE_APP
from nose.tools import raises, assert_equals
from splinter.request_handler.status_code import HttpResponseError

class StatusCodeTest(object):

    @raises(HttpResponseError)
    def test_should_visit_an_absent_page_and_get_an_404_error(self):
        "Should visit an absent page and get an 404 error"
        self.browser.visit(EXAMPLE_APP + "this_page_does_not_exists")

    def test_should_visit_index_of_example_app_and_get_200_status_code(self):
        self.browser.visit(EXAMPLE_APP)
        assert_equals(200, self.browser.status_code)
