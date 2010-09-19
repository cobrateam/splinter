import unittest
from should_dsl import should
from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from time import sleep

class BrowserTest(unittest.TestCase):

    def test_can_open_page(self):
        "should be able to visit, get title and quit"
        browser = Browser()
        page = browser.visit(EXAMPLE_APP)
        title = page.title
        browser.quit()
        title |should| equal_to('Example Title')

    def test_submiting_a_form_and_verifying_page_content():
        "should be able search a term in google and verifying if content expected exists"
        browser = Browser()
        page = browser.visit('http://google.com')
        page.fill_in('q', 'andrews medina')

        sleep(5)

        content = page.content

        browser.quit()

        assert 'www.andrewsmedina.com' in page.content

