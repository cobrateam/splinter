from splinter.browser import Browser

def test_can_open_page():
    browser = Browser()
    page = browser.visit('http://google.com')
    
    title = page.get_title()
    
    browser.quit()
    
    assert 'Google' == title