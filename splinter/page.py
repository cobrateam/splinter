class Page(object):
    
    def __init__(self, url, browser):
        self.url = url
        self.browser = browser
    
    @property
    def title(self):
        return self.browser.driver.title
    