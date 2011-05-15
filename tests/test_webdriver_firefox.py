import os
import unittest

from nose.tools import assert_equals
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from base import WebDriverTests


class FirefoxBrowserTest(WebDriverTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('webdriver.firefox')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()

    def test_attach_file(self):
        "should provide a way to change file field value"
        file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'mockfile.txt')
        self.browser.attach_file('file', file_path)
        self.browser.find_by_name('upload').first.click()

        html = self.browser.html
        assert 'text/plain' in html
        assert open(file_path).read() in html

    def test_access_alerts_and_accept_them(self):
        self.browser.visit('http://localhost:5000/alert')
        self.browser.find_by_tag('h1').first.click()
        alert = self.browser.get_alert()
        assert_equals(alert.text, 'This is an alert example.')
        alert.accept()

    def test_access_prompts_and_be_able_to_fill_then(self):
        self.browser.visit('http://localhost:5000/alert')
        self.browser.find_by_tag('h2').first.click()

        alert = self.browser.get_alert()
        assert_equals(alert.text, 'What is your name?')
        alert.fill_with('Splinter')
        alert.accept()

        response = self.browser.get_alert()
        assert_equals(response.text, 'Splinter')
        response.accept()

    def test_access_alerts_using_with(self):
        "should access alerts using 'with' statement"
        self.browser.visit('http://localhost:5000/alert')
        self.browser.find_by_tag('h1').first.click()
        with self.browser.get_alert() as alert:
            assert_equals(alert.text, 'This is an alert example.')
            alert.accept()
