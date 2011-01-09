import unittest
from should_dsl import should, should_not
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import BaseBrowserTests

import os

class FirefoxBrowserTest(BaseBrowserTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser()

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        
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
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').click()
    
        html = self.browser.html
        html |should| include('text/plain')
        html |should| include(open(file_path).read())
