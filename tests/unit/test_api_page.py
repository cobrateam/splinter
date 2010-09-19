import unittest
from splinter.page import Page
from ludibrio import Stub

class PageTest(unittest.TestCase):

    def test_should_have_title(self):

        with Stub() as driver:
            driver.title >> 'foo title'
        page = Page('http://example.com', driver)
        assert page.title == 'foo title'
