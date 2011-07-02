import os
import unittest
from splinter.browser import Browser
from base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP
from nose.tools import assert_equals, raises

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
        assert 'text/plain' in html
        assert open(file_path).read() in html

    def test_forward_to_none_page(self):
        "should not fail when trying to forward to none"
        browser = Browser('zope.testbrowser')
        browser.visit(EXAMPLE_APP)
        browser.forward()
        assert_equals(EXAMPLE_APP, browser.url)
        browser.quit()

    @raises(NotImplementedError)
    def test_cant_switch_to_frame(self):
        "zope.testbrowser should not be able to switch to frames"
        self.browser.get_iframe('frame_123')

    def test_create_and_access_a_cookie(self):
        "should be able to create and access a cookie"
        self.browser.add_cookie({'sha': 'zam'})
        assert_equals(self.browser.cookie('sha'), 'zam')

    def test_create_some_cookies_and_delete_them_all(self):
        "should be able to delete all cookies"
        self.browser.add_cookie({'whatever': 'and ever'})
        self.browser.add_cookie({'anothercookie': 'im bored'})
        self.browser.delete_cookies()
        assert_equals(self.browser.cookies, {})

    def test_create_and_delete_a_cookie(self):
        "should be able to create and destroy a cookie"
        self.browser.delete_cookies()
        self.browser.add_cookie({'cookie': 'with milk'})
        self.browser.delete_cookie('cookie')
        assert_equals(self.browser.cookies, {})

    def test_try_to_destroy_an_absent_cookie_and_nothing_happens(self):
        self.browser.delete_cookies()
        self.browser.add_cookie({'foo': 'bar'})
        self.browser.delete_cookie('mwahahahaha')
        assert_equals(self.browser.cookies, {'foo': 'bar'})
