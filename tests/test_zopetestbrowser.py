import unittest
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import BaseBrowserTests

class ZopeTestBrowserDriverTest(BaseBrowserTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser('zope.testbrowser')
        self.browser.visit(EXAMPLE_APP)

    def tearDown(self):
        self.browser.quit()
        
