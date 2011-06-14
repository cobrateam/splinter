import unittest
from base import BaseBrowserTests
from fake_webapp import EXAMPLE_APP
from splinter.browser import Browser

class SpynnerTest(BaseBrowserTests, unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('phantomjs')

    def setUp(self):
        self.browser.visit(EXAMPLE_APP)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
