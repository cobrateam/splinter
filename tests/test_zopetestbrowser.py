import unittest
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import BaseBrowserTests
from should_dsl import should

import os

class ZopeTestBrowserDriverTest(BaseBrowserTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser('zope.testbrowser')
        self.browser.visit(EXAMPLE_APP)

    def tearDown(self):
        self.browser.quit()
        
    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').click()
    
        html = self.browser.html
        html |should| include('text/plain')
        html |should| include(open(file_path).read())
