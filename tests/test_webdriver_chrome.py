import unittest
from should_dsl import should
from splinter.browser import Browser
from fake_webapp import start_server, stop_server
from base import WebDriverTests

class ChromeBrowserTest(WebDriverTests, unittest.TestCase):

    def setUp(self):
        self.browser = Browser('webdriver.chrome')
        start_server(self.browser)

    def tearDown(self):
        stop_server()

    def test_attach_file_is_not_implemented(self):
        "attach file is no implemented for chrome driver"
        (self.browser.attach_file, 'file', 'file_paht') |should| throw(NotImplementedError)
