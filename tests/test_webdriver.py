import unittest
from should_dsl import should, should_not
from splinter.browser import Browser
from fake_webapp import start_server, stop_server
from base import BaseBrowserTests

class BrowserTest(BaseBrowserTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser()
        start_server(self.browser)

    def tearDown(self):
        stop_server()
        
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
    
