from base import BaseBrowserTests
from should_dsl import should, should_not

class WebDriverTests(BaseBrowserTests):

    def test_can_execute_javascript(self):
        "should execute javascript"
        self.browser.execute_script("$('body').empty()")
        self.browser.find_by_tag("body") == ""

    def test_can_evaluate_script(self):
        "should evaluate script"
        assert self.browser.evaluate_script("4+4") == 8

    def test_can_verify_if_a_element_is_visible(self):
        "should provide verify if element is visible"
        self.browser.find_by_id("visible") |should| be_visible

    def test_can_verify_if_a_element_is_invisible(self):
        "should provide verify if element is invisible"
        self.browser.find_by_id("invisible") |should_not| be_visible

    def test_attach_file(self):
        self.fail("You should implement test_attach_file method")
