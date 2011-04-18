from nose.tools import assert_true

class StatusCode404Test(object):
    def test_should_visit_an_absent_page_and_get_an_404_error(self):
        "Should visit an absent page and get an 404 error"
        self.browser.visit("http://localhost:5000/this_page_does_not_exists")
        assert_true(False)
