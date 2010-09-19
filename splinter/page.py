class Page(object):
    
    def __init__(self, url, browser):
        self.url = url
        self.browser = browser
    
    def get_title(self):
        return self.browser.driver.get_title()
    