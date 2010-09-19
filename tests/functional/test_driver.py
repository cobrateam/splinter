from splinter.browser import Browser
from fake_webapp import EXAMPLE_APP
from time import sleep

def test_can_open_page():
    browser = Browser()
    page = browser.visit(EXAMPLE_APP)
    title = page.title
    browser.quit()
    assert 'Example Title' == title
    
def test_submiting_a_form_and_verifying_page_content():
    browser = Browser()
    page = browser.visit('http://google.com')
    page.fill_in('q', 'andrews medina')
    
    sleep(5)
    
    content = page.content
    
    browser.quit()

    assert 'www.andrewsmedina.com' in page.content