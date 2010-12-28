import unittest
from splinter.browser import Browser
from base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP, start_server, stop_server

class ZopeTestBrowserDriverTest(BaseBrowserTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser('zope.testbrowser')
        start_server(self.browser)
        #self.browser.visit(EXAMPLE_APP)

    def tearDown(self):
        stop_server()
        #self.browser.quit() 



