import unittest
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests
from nose.tools import raises


class ChromeBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('webdriver.chrome')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    @raises(NotImplementedError)
    def test_attach_file_is_not_implemented(self):
        "attach file is not implemented for chrome driver"
        self.browser.attach_file('file', 'file_path')

    @raises(NotImplementedError)
    def test_access_alerts_and_accept_them(self):
        "should raise NotImplementedError when trying to access alerts"
        alert = self.browser.get_alert()

    @raises(NotImplementedError)
    def test_access_prompts_and_be_able_to_fill_then(self):
        "should raise NotImplementedError when trying to access prompts"
        alert = self.browser.get_alert()

    @raises(NotImplementedError)
    def test_access_alerts_using_with(self):
        "should raise NotImplementedError when trying to access alerts/promps using 'with'"
        with self.browser.get_alert() as alert:
            pass
