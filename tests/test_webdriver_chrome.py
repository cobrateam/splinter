import unittest
from should_dsl import should
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests

class ChromeBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('webdriver.chrome')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_attach_file_is_not_implemented(self):
        "attach file is no implemented for chrome driver"
        (self.browser.attach_file, 'file', 'file_paht') |should| throw(NotImplementedError)
