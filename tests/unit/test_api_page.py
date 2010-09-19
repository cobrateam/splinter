import unittest
from splinter.page import Page
from ludibrio import Stub
from should_dsl import should

class PageTest(unittest.TestCase):

    def test_should_have_title(self):

        with Stub() as driver:
            driver.title >> 'foo title'
        page = Page('http://example.com', driver)
        page.title |should| equal_to('foo title')
