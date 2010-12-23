import unittest
from splinter.browser import Browser
from base import BaseBrowserTests
from fake_webapp import start_server, stop_server

class ZopeTestBrowserDriverTest(BaseBrowserTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser('zope.testbrowser')
        start_server(self.browser)

    def tearDown(self):
        stop_server()
        
