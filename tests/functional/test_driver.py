import unittest
from should_dsl import should
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP


class BrowserTest(unittest.TestCase):

    def test_can_open_page(self):
        "should be able to visit, get title and quit"
        browser = Browser()
        page = browser.visit(EXAMPLE_APP)
        title = page.title
        browser.quit()
        title |should| equal_to('Example Title')
