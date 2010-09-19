from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP

def test_can_open_page():
    browser = Browser()
    page = browser.visit(EXAMPLE_APP)
    title = page.title
    browser.quit()
    assert 'Example Title' == title
