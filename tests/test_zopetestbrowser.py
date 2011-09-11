from splinter.browser import Browser
from base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP
from nose.tools import assert_equals, raises

import os
import unittest


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

    def test_cant_switch_to_frame(self):
        "zope.testbrowser should not be able to switch to frames"
        try:
            self.browser.get_iframe('frame_123')
            self.fail()
        except NotImplementedError as e:
            assert_equals("zope.testbrowser does not support frames", e.args[0])

    @raises(NotImplementedError)
    def test_simple_type(self):
        "zope.testbrowser won't support type method because it doesn't interact with Javascritp, and this is the meaning of that method"
        self.browser.type('query',' with type method')

    @raises(NotImplementedError)
    def test_slowly_typing(self):
        "zope.testbrowser won't support type method because it doesn't interact with Javascritp, and this is the meaning of that method"
        self.browser.type('query',' with type method', slowly=True)

    @raises(NotImplementedError)
    def test_cant_mouseover(self):
        "zope.testbrowser should not be able to put the mouse over the element"
        self.browser.find_by_css('#visible').first.mouse_over()

    @raises(NotImplementedError)
    def test_cant_mouseout(self):
        "zope.testbrowser should not be able to mouse out of an element"
        self.browser.find_by_css('#visible').first.mouse_out()
