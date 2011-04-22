from nose.tools import raises
from splinter.request_handler.request_handler import PageNotFound

class StatusCode404Test(object):
    @raises(PageNotFound)
    def test_should_visit_an_absent_page_and_get_an_404_error(self):
        "Should visit an absent page and get an 404 error"
        self.browser.visit("http://localhost:5000/this_page_does_not_exists")
