import unittest
from splinter.browser import Browser
from base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP
from should_dsl import should

import os

class ZopeTestBrowserDriverTest(BaseBrowserTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('zope.testbrowser')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(self):
        self.browser.quit()

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').first.click()

        html = self.browser.html
        html |should| include('text/plain')
        html |should| include(open(file_path).read())
