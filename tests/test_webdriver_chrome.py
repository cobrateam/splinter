import unittest
from should_dsl import should, should_not
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import BaseBrowserTests

class ChromeBrowserTest(BaseBrowserTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser('chrome')
        self.browser.visit(EXAMPLE_APP)

    def tearDown(self):
        self.browser.quit()
        
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

    def test_attach_file_is_not_implemented(self):
        "attach file is no implemented for chrome driver"
        (self.browser.attach_file, 'file', 'file_paht') |should| throw(NotImplementedError)