import unittest
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import BaseBrowserTests

# class BrowserTest(BaseBrowserTests, unittest.TestCase):
# 
#     def setUp(self):
#         self.browser = Browser()
#         self.browser.visit(EXAMPLE_APP)
# 
#     def tearDown(self):
#         self.browser.quit()
#         
#     def test_can_execute_javascript(self):
#         "should execute javascript"
#         self.browser.execute_script("$('body').empty()")
#         self.browser.find_by_tag("body") == ""
#         
#     def test_can_evaluate_script(self):
#         "should evaluate script"
#         assert self.browser.evaluate_script("4+4") == 8
#         
