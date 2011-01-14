import unittest
from splinter.browser import Browser
from base import BaseBrowserTests
from fake_webapp import start_server, stop_server
from should_dsl import should

import os

class ZopeTestBrowserDriverTest(BaseBrowserTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser('zope.testbrowser')
        start_server(self.browser)

    def tearDown(self):
        stop_server()
        
    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').click()
    
        html = self.browser.html
        html |should| include('text/plain')
        html |should| include(open(file_path).read())
