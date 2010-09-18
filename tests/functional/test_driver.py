from splinter.driver import WebDriver

def test_can_open_page():
    browser = WebDriver()
    browser.visit('http://google.com')
    
    title = browser.get_title()
    
    browser.quit()
    
    assert 'Google' == title