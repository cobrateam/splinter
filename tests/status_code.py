from fake_webapp import EXAMPLE_APP
from splinter.request_handler.status_code import HttpResponseError


class StatusCodeTest(object):

    def test_should_visit_an_absent_page_and_get_an_404_error(self):
        with self.assertRaises(HttpResponseError):
            self.browser.visit(EXAMPLE_APP + "this_page_does_not_exists")

    def test_should_visit_index_of_example_app_and_get_200_status_code(self):
        self.browser.visit(EXAMPLE_APP)
        self.assertEquals(200, self.browser.status_code)
