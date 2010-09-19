class Page(object):
    
    def __init__(self, url, driver):
        self.url = url
        self.driver = driver
    
    @property
    def title(self):
        return self.driver.title
    
    @property
    def content(self):
        return self.driver.source
        
    def fill_in(self, name, value):
        element = self.driver.find("q")
        element.send_keys(value)
        element.submit()
        