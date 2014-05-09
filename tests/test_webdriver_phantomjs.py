import unittest

from splinter import Browser
from .fake_webapp import EXAMPLE_APP
from .base import WebDriverTests


class PhantomJSBrowserTest(WebDriverTests, unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser("phantomjs")

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    def test_get_alert(self):
        with self.assertRaises(NotImplementedError):
            self.browser.get_alert()

    def test_right_click(self):
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').right_click()

    def test_double_click(self):
        with self.assertRaises(NotImplementedError):
            self.browser.find_by_id('visible').double_click()

    def test_access_prompts_and_be_able_to_fill_then(self):
        with self.assertRaises(NotImplementedError):
            self.browser.get_alert()

    def test_access_confirm_and_accept_and_dismiss_them_using_with(self):
        with self.assertRaises(NotImplementedError):
            self.browser.get_alert()

    def test_access_confirm_and_accept_and_dismiss_them(self):
        with self.assertRaises(NotImplementedError):
            self.browser.get_alert()

    def test_access_alerts_using_with(self):
        with self.assertRaises(NotImplementedError):
            self.browser.get_alert()

    def test_access_alerts_and_accept_them(self):
        with self.assertRaises(NotImplementedError):
            self.browser.get_alert()

    def test_can_work_on_popups(self):
        # FIXME: Check https://github.com/detro/ghostdriver/issues/180 to see if
        # we can implement this test
        pass


class PhantomJSBrowserTestWithCustomHeaders(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        custom_headers = {'X-Splinter-Customheaders-1': 'Hello',
                          'X-Splinter-Customheaders-2': 'Bye'}
        cls.browser = Browser("phantomjs", custom_headers=custom_headers)

    def test_create_a_phantomjs_with_custom_headers(self):
        self.browser.visit(EXAMPLE_APP + 'headers')
        self.assertTrue(
            self.browser.is_text_present('X-Splinter-Customheaders-1: Hello'))
        self.assertTrue(
            self.browser.is_text_present('X-Splinter-Customheaders-2: Bye'))

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
